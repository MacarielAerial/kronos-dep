from pathlib import Path

from kronos.data_interfaces.networkx_graph_data_interface import NetworkXGraphDataInterface
from kronos.data_interfaces.spacy_pipeline_data_interface import SpacyPipelineDataInterface
from kronos.nodes.semantics_graph import augment_nx_g_with_semantics

def mixed_layout_nx_g_to_semantics_nx_g(path_mixed_layout_nx_g: Path, 
                                        path_spacy_pipeline: Path,
                                        path_semantics_nx_g: Path) -> None:
    # Data Access - Input
    mixed_layout_nx_g_data_interface = NetworkXGraphDataInterface(filepath=path_mixed_layout_nx_g)
    mixed_layout_nx_g = mixed_layout_nx_g_data_interface.load()

    spacy_pipeline_data_interface = SpacyPipelineDataInterface(filepath=path_spacy_pipeline)
    spacy_pipeline = spacy_pipeline_data_interface.load()

    # Task Processing
    semantics_nx_g = augment_nx_g_with_semantics(nx_g=mixed_layout_nx_g, spacy_pipeline=spacy_pipeline)

    # Data Access - Output
    semantics_nx_g_data_inteface = NetworkXGraphDataInterface(filepath=path_semantics_nx_g)
    semantics_nx_g_data_inteface.save(nx_g=semantics_nx_g)


if __name__ == "__main__":
    import argparse

    from kronos.nodes.project_logging import default_logging

    default_logging()

    parser = argparse.ArgumentParser(
        description="Augments a layout networkx graph with mixed node types "
        "with semantic information such as NER"
    )
    parser.add_argument(
        "-pmlng",
        "--path_mixed_layout_nx_g",
        required=True,
        type=Path,
        help="Path from which a mixed node type layout networkx graph is loaded"
    )
    parser.add_argument(
        "-psp",
        "--path_spacy_pipeline",
        type=Path,
        required=True,
        help="Path from which a spacy pipeline (Language) object is loaded"
    )
    parser.add_argument(
        "-psng",
        "--path_semantics_nx_g",
        type=Path,
        required=True,
        help="Path to which a semantics-augmented networkx graph is saved"
    )

    args = parser.parse_args()

    mixed_layout_nx_g_to_semantics_nx_g(
        path_mixed_layout_nx_g=args.path_mixed_layout_nx_g,
        path_spacy_pipeline=args.path_spacy_pipeline,
        path_semantics_nx_g=args.path_semantics_nx_g
    )

