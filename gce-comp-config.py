# config.py
## run jobs on compute nodes 
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
            # Ensure that the working dir is writeable from the compute nodes,
            # for eg. paths below /gpfs/alpine/world-shared/
#            working_dir='$WORK_DIR', # YOUR_WORKING_DIR_ON_SHARED_FS,
#            cores_per_node=1,
            address=address_by_interface('ens5f0'),  # This assumes Parsl is running on login node
            #worker_port_range=(50000, 55000),
            provider=LSFProvider(
                launcher=SingleNodeLauncher(),
                walltime="00:30:00",
#                nodes_per_block=2,
                nodes_per_block=1,
                init_blocks=1,
                max_blocks=1,
                queue="standard",
                worker_init='''module load conda; conda activate /rs1/researchers/j/jfossot/conda_env''',
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
    "organization": "NC State University",
    "department": "Research Computing",
    "public": False,
    "visible_to": [],
}
