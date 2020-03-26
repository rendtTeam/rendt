# rendt

To use our app you should:
1. connect to the EC2 instance, go to `/stable_server`, run `nohup python3 server.py 23456 > nohup.out 2>&1 &`
2. make sure the port numbers in `sender.py` and `receiver.py` match that of the server (23456 in this case)
3. run 'ui.py'.For this you should download 2 external class "PyQt5" and "psutil" and have 2 instances of the ui.py (either 2 running applications on a single computer or 1 application on 2 computers)

## Workflow:
**Sender** does: 
1. `send-perm` - get permission from the server to upload an executable (currently the path to the executable is fixed but it too can be changed to be prompted as an input). returns: `job_id`, `db_token`
2. `send-up` - upload the executable file, now that we have permission (and token). enter the `job_id` and `db_token` obtained at the prev step when prompted. returns: none
**Receiver** does:
3. `get` - get the list of available to execute jobs on the server. returns: list of `job_id`s
4. `exec-perm` - get permission from the server to download an executable specified by `job_id`. returns: `db_token`, `file_size`
5. `exec-down` - download the executable, now that we have permission (and token). enter the token and size from prev step when prompted. returns: none
6. `exec` - execute the executable locally and produce the output file (currently the path to the output file is fixed but it too can be changed to be prompted as an input). returns: none
7. `out-perm` - get permission from the server to upload an output of the job specified by its `job_id` (currently the path to the output is fixed but it too can be changed to be prompted as an input). returns: `db_token`
8. `out-up` - upload the output file, now that we have permission (and token). enter the `job_id` and `db_token` obtained at the prev steps when prompted. returns: none
(8*) `exit` - stops the cli and exits program
**Sender** does: 
9. `down-perm` - get permission from the server to download the output to a job submitted by the sender, specified by `job_id` (return way earlier). returns: `db_token`, `file_size`. returns: none
10. `down` - download the output file, now that we have permission (and token). enter the token and size from prev step when prompted. returns: none

That's it!  
Note: these steps can probably tried in different orders; for example, the sender can ask the server for the output of its job *before* some receiver has actually uploaded it, and will receive an error message in this case (the server will not crash in this case). However, most of such scenarios haven't been tested yet, so some unforeseen crashes are possible in case of different execution paths.

