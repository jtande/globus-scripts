# NCSU PSI Globus Automation 
Simple code for various use cases using Globus.
Credit to [jaswilli](https://github.com/globus/native-app-examples)
## Overview

There are three example use cases in this repo:

* Syncing a directory.
* Syncing timer for data in a shared directory.
* Globus compute sample function .
* Globus compute configuration for running jobs on login node (for testing only)
* Globus compute configuration for running jobs on compute nodes


The Python codes are built using the 
[Globus SDK](https://globus-sdk-python.readthedocs.io/en/stable/).
* [`globus_folder_sync.py`](globus_folder_sync.py): submits a recursive transfer with sync option; uses a [Native App grant](https://github.com/globus/native-app-examples).
* [`globus_folder_sync_timer.py`](globus_folder_sync_timer.py): submits an automated recursive transfer with sync option; After the completion of the first task, the transfer will be executed every midnight EST
* [`gce-login-config.py`](gce-login-config.py): submits a globus finction on the HPC login node;
* [`gce-login-config.py`](gce-login-config.py): submits a globus finction on the HPC compute node;



## Getting Started
* Install the [Globus Command Line Interface (CLI)](https://docs.globus.org/cli/installation/).
* Set up your environment.
    * [OS X](#os-x)
    * [Linux](#linux-ubuntu)
    * [Windows](#windows)
* Create a Native App registration for use by visiting the [Globus Developer Pages](https://developers.globus.org).
* Replace the UUIDs  in [`globus_folder_sync.py`](globus_folder_sync.py) and [`globus_folder_sync_timer.py`](globus_folder_sync_timer.py).


### OS X

##### Environment Setup

* `sudo easy_install pip`
* `sudo pip install virtualenv`
* `git clone https://github.com/jtande/globus-scripts`
* `cd automation-examples`
* `virtualenv venv`
* `source venv/bin/activate`
* `pip install -r requirements.txt`

### Linux (Ubuntu)

##### Environment Setup

* `sudo apt-get update`
* `sudo apt-get install python-pip`
* `sudo pip install virtualenv`
* `sudo apt-get install git`
* `git clone https://github.com/jtande/globus-scripts`
* `cd globus-scripts`
* `virtualenv venv`
* `source venv/bin/activate`
* `pip install -r requirements.txt`

### Windows

##### Environment Setup

* Install Python (<https://www.python.org/downloads/windows/>)
* `pip install virtualenv`
* Install git (<https://git-scm.com/downloads>)
* `git clone https://github.com/jtande/globus-scripts`
* `cd globus-scripts`
* `virtualenv venv`
* `venv\Scripts\activate`
* `pip install -r requirements.txt`

## Running the scripts
[`globus_folder_sync.py`](globus_folder_sync.py) and [`globus_folder_sync_timer.py`](globus_folder_sync_timer.py) are executed as follow:<br>
<the-script.py> -h <br>
will return the arguments and the default values

### globus_folder_sync.py 

**Note**: Both ./globus_folder_sync.py and ./globus_folder_sync_timer.py require you to login (see Login section for help).

