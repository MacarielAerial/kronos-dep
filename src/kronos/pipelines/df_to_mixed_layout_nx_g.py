from pathlib import Path
from kronos.data_interfaces.networkx_graph_data_interface import NetworkXGraphDataInterface

from kronos.data_interfaces.timetable_df_data_interface import TimeTableDFDataInterface
from kronos.nodes.layout_graph import df_to_layout_nx_g

def df_to_mixed_layout_nx_g(path_df_timetable: Path, path_mixed_layout_nx_g: Path) -> None:
    # Data Access - Input
    timetable_data_interface = TimeTableDFDataInterface(filepath=path_df_timetable)
    df_timetable = timetable_data_interface.load()

    # Task Processing
    layout_nx_g = df_to_layout_nx_g(df=df_timetable)

    # Data Access - Output
    networkx_graph_data_interface = NetworkXGraphDataInterface(filepath=path_mixed_layout_nx_g)
    networkx_graph_data_interface.save(nx_g=layout_nx_g)


if __name__ == "__main__":
    import argparse

    from kronos.nodes.project_logging import default_logging

    default_logging()

    parser = argparse.ArgumentParser(
        description="Parses a visibility layout graph from a timetable dataframe"
    )
    parser.add_argument(
        "-pdt",
        "--path_df_timetable",
        type=Path,
        required=True,
        help="Path from which a serialised timetable is loaded"
    )
    parser.add_argument(
        "-pmlng",
        "--path_mixed_layout_nx_g",
        required=True,
        type=Path,
        help="Path to which a mixed layout networkx graph is saved"
    )

    args = parser.parse_args()

    df_to_mixed_layout_nx_g(path_df_timetable=args.path_df_timetable,
                            path_mixed_layout_nx_g=args.path_mixed_layout_nx_g)
