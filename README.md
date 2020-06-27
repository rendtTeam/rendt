
# rendt

To use our app you should:
1. clone this reposotory to your local machine
2. navigate to src/client and run `python3 ui.py`. For this you may need to download some external libraries. To download and install necessary packages run `pip install -r requirements.txt` command in the `rendt` directory.

## Guidelines for Renters:
Renters who wish to submit a job to be executed have to follow a few basic guidelines.
1. All files pertaining to the job must be collected in a single folder named `files`. A bash script called `run.sh` must be included in this folder that would run the job as the renter wants, as if they were running it on a linux terminal.
2. The `files` folder (not the contents, but the folder) must be zipped; this is the execution file you have to submit for successful execution.

#### Official [Website](https://rendtapp.github.io/)

## Screenshots 

##### Dashboard: see submitted and received jobs

![Dashboard](https://github.com/rendtTeam/rendt/blob/master/screenshots/dashboard.png)
##### Lease: set an hourly price and mark your account as a leaser

![Lease](https://github.com/rendtTeam/rendt/blob/master/screenshots/lease.png)

##### Rent: select files to upload

![Select files to upload](https://github.com/rendtTeam/rendt/blob/master/screenshots/upload-files.png)
##### Rent: select a leaser

![Select a leaser](https://github.com/rendtTeam/rendt/blob/master/screenshots/rental-submission.png)
##### Status of the received job on the leaser machine

![Status: leaser](https://github.com/rendtTeam/rendt/blob/master/screenshots/executing.png)

##### Status of the submitted job seen from the renter's side

![Status: renter](https://github.com/rendtTeam/rendt/blob/master/screenshots/job-status.png)
