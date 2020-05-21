import sys
import json
import io
import struct
import socket, ssl

server_addr = ('18.220.165.22', 23456)

class Messaging:
    def __init__(self, sock, addr, request):
        self.sock = sock
        self.addr = addr
        self.request = request
        self._recv_buffer = b''
        self._send_buffer = b''
        self._request_queued = False
        self._jsonheader_len = None
        self.jsonheader = None
        self.response = None
        # self.response_created = False

    def _read(self):
        try:
            data = self.sock.recv(16384)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError('Peer closed.')

    def _write(self):
        if self._send_buffer:
            print('sending', repr(self._send_buffer), 'to', self.addr)
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]


    def _json_encode(self, obj):
        return json.dumps(obj, ensure_ascii=False).encode('utf-8')

    def _json_decode(self, json_bytes):
        tiow = io.TextIOWrapper(io.BytesIO(json_bytes), encoding='utf-8', newline='')
        obj = json.load(tiow)
        tiow.close()
        return obj

    def _create_message(self, content_bytes, content_type):
        jsonheader = {
            'byteorder': sys.byteorder,
            'content-length': len(content_bytes),
            'content-type': content_type,
        }
        jsonheader_bytes = self._json_encode(jsonheader)
        message_hdr = struct.pack('>H', len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + content_bytes
        return message

    def read(self):
        self._read()

        if self._jsonheader_len is None:
            self.process_protoheader()

        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self.process_jsonheader()

        if self.jsonheader:
            if self.response is None:
                self.process_response()

    def write(self):
        if not self._request_queued:
            self.queue_request()

        self._write()

    def queue_request(self):
        content = self.request["content"]
        content_type = self.request["type"]
        if content_type == "text/json":
            req = {
                "content_bytes": self._json_encode(content),
                "content_type": content_type,
            }
        else:
            req = {
                "content_bytes": content,
                "content_type": content_type,
            }
        message = self._create_message(**req)
        self._send_buffer += message
        self._request_queued = True

    def process_protoheader(self):
        hdrlen = 2
        if len(self._recv_buffer) >= hdrlen:
            self._jsonheader_len = struct.unpack('>H', self._recv_buffer[:hdrlen])[0]
            self._recv_buffer = self._recv_buffer[hdrlen:]

    def process_jsonheader(self):
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            self.jsonheader = self._json_decode(self._recv_buffer[:hdrlen])
            self._recv_buffer = self._recv_buffer[hdrlen:]
            for reqhdr in (
                'byteorder',
                'content-length',
                'content-type'
            ):
                if reqhdr not in self.jsonheader:
                    raise ValueError(f'Missing required header {reqhdr}.')

    def process_response(self):
        content_len = self.jsonheader['content-length']
        if not len(self._recv_buffer) >= content_len:
            return # TODO
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        if self.jsonheader['content-type'] == 'text/json':
            self.response = self._json_decode(data)
            print('received response', repr(self.response), 'from', self.addr)
        else:
            # Binary or unknown content-type
            self.response = data
            print(f'received {self.jsonheader["content-type"]} response from', self.addr)

    def close(self):
        print('closing connection to', self.addr)

        try:
            self.sock.close()
        except OSError as e:
            print('error: socket.close() exception for', f'{self.addr}: {repr(e)}')
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None
