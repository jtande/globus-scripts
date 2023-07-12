#############################################################
#
#
#  This configuration file will allow access to the compute
#  nodes on the Hazel HPC Cluster at North Carolina State 
#  University.
# 
#
#############################################################
from globus_compute_endpoint.endpoint.utils.config import Config
from globus_compute_endpoint.executors import HighThroughputExecutor

from parsl.launchers import SingleNodeLauncher
from parsl.providers import LSFProvider

from parsl.addresses import address_by_interface

config = Config(
    display_name=None,  # If None, defaults to the endpoint name
    executors=[
        HighThroughputExecutor(
            label='Hazel_HTEX', # Label for this execution instance
            address=address_by_interface('ens5f0'),  # This assumes Parsl is running on login node
            #worker_port_range=(50000, 55000),
            provider=LSFProvider(
                launcher=SingleNodeLauncher(),
                walltime="00:30:00",
#                nodes_per_block=2,
                nodes_per_block=1,
                init_blocks=1,
                max_blocks=1,
                queue="standard",    # change this to any queue that meets your function's need
                # worker_init prepares the compute environment
                worker_init='''module load conda; conda activate /path/to/your/condaenv/conda_env''',
                scheduler_options="#BSUB -R span[hosts=1]",  # Confined requested cores to a single node
#                project='PSI Globus Compute',
                cores_per_node=12,
                cmd_timeout=60
            ),
        ),
    ]
)

# For now, visible_to must be a list of URNs for globus auth users or groups, e.g.:
# urn:globus:auth:identity:{user_uuid}
# urn:globus:groups:id:{group_uuid}
meta = {
    "name": "ncsu-gce-jfossot",
    "description": "Test Profile",
    "organization": "North Carolina State University",
    "department": "Research Computing",
    "public": False,
    "visible_to": [],
}
