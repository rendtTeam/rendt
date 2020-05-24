# rendt

To use our app you should:
1. connect to the EC2 instance, go to `/stable_server`, run `nohup python3 server.py 23456 > nohup.out 2>&1 &`
2. make sure the port numbers in `sender.py` and `receiver.py` match that of the server (23456 in this case)
3. run 'ui.py'. For this you should download 3 external libraries, namely, "pyqt5", "pyqt5-tools" and "psutil" and have an instance of the ui.py (either 1 running application on a single computer being renter and leaser at the same time and on same machine or 1 application on 2 computers)

## Workflow:
Create a working directory containing all the files you need for the job. Write a `bash` script to run your job, and include it with the rest of the files (in the root folder of your working directory). Then, zip this root directory and submit as a job. After your job is uploaded, save the `job_id`, and use it to later retrieve your results.

### Codes for Job statuses in the database:
`a`: available  
`ix`: in execution  
`xtbu`: executable to be uploaded  
`otbu`: output file(s) to be uploaded  
`f`: finished  
`xuf`: executable upload failed  
