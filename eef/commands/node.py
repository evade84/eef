from typer import Typer, style

from eef import const, output
from eef.config import config
from eef.node_client import NodeClient

app = Typer()


@app.callback(invoke_without_command=True)
def node_info():
    node = NodeClient().node()
    if node.version in const.COMPATIBLE_NODE_VERSIONS:
        compatibility = style("(compatible)", fg="green")
    else:
        compatibility = style("(incompatible)", fg="black", bg="red")
    output.info(
        f"evade84-node {node.version} {compatibility}: {node.name} at {config.read_node_url()}."
    )
