import logging

from networkx import Graph

from kronos.nodes.graph_schema import NodeAttrKey, NodeType

logger = logging.getLogger(__name__)


def delete_node_attr(nx_g: Graph, node_attr_key: NodeAttrKey) -> Graph:
    n_deleted = 0
    for nid, attrs in nx_g.nodes.data():
        if node_attr_key.value in attrs.keys():
            del nx_g.nodes[nid][node_attr_key.value]

            n_deleted += 1

    logger.info(f"{n_deleted} instances of node attribute {node_attr_key.value} "
                "have been deleted")
    
    return nx_g

def delete_node_of_type(nx_g: Graph, ntype: NodeType) -> Graph:
    n_deleted = 0
    for nid, attrs in nx_g.nodes.data():
        if attrs[NodeAttrKey.ntype.value] == ntype:
            del nx_g.nodes[nid]
    
    logger.info(f"{n_deleted} instances of {ntype.value} nodes have been deleted")

    return nx_g
