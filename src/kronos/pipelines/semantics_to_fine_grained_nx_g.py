from pathlib import Path

from networkx import DiGraph

from kronos.data_interfaces.networkx_graph_data_interface import NetworkXGraphDataInterface
from kronos.nodes.layout_graph import derive_fine_grained_edge_tuples
from kronos.nodes.semantics_graph import fine_grained_node_tuples_from_semantics_nx_g

def _semantics_to_fine_grained_nx_g(semantics_nx_g: DiGraph) -> DiGraph:
    # Collect fine grained graph elements
    fine_grained_node_tuples = fine_grained_node_tuples_from_semantics_nx_g(semantics_nx_g)
    fine_grained_edge_tuples = derive_fine_grained_edge_tuples(semantics_nx_g, fine_grained_node_tuples)

    # Construct fine grained graph
    fine_grained_nx_g = DiGraph()
    fine_grained_nx_g.update(edges=fine_grained_edge_tuples, nodes=fine_grained_node_tuples)

    return fine_grained_nx_g
    

def semantics_to_fine_grained_nx_g(path_semantics_nx_g: Path, path_fine_grained_nx_g: Path) -> None:
    # Data Access - Input
    semantics_nx_g_data_interface = NetworkXGraphDataInterface(filepath=path_semantics_nx_g)
    semantics_nx_g = semantics_nx_g_data_interface.load()

    # Task Processing
    fine_grained_nx_g = _semantics_to_fine_grained_nx_g(semantics_nx_g=semantics_nx_g)

    # Data Access - Output
    ...
