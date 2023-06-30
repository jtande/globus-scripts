#! /home/jacob/globus-compute-endpt/venv/bin/python 
from globus_compute_sdk import Executor


def batch_job_done():
    import subprocess
    Hostname = subprocess.run(["hostname"],stdout=subprocess.PIPE, text=True)
    return Hostname

ncsu_endpoint = '566f1cb6-4472-47cf-886c-91575ddb9c30'
with Executor(endpoint_id=ncsu_endpoint) as gce:
    fut = gce.submit(batch_job_done)
    print("\n Curent work dir is:")
    print(fut.result())


