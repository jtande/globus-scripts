# config.py
# run jobs on login nodes
from globus_compute_endpoint.endpoint.utils.config import Config
from globus_compute_endpoint.executors import HighThroughputExecutor
from parsl.providers import LocalProvider

config = Config(
    executors=[
        HighThroughputExecutor(
            provider=LocalProvider(init_blocks=1, min_blocks=0, max_blocks=1),
        )
    ],
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
