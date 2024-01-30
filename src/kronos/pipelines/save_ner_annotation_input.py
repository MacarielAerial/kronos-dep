from pathlib import Path

from kronos.data_interfaces.timetable_df_data_interface import TimeTableDFDataInterface

def save_ner_annotation_input(path_df_timetable: Path, path_ner_annotation_input: Path) -> None:
    # Data Access - Input
    timetable_data_interface = TimeTableDFDataInterface(filepath=path_df_timetable)
    df_timetable = timetable_data_interface.load()

    # Task Processing & Data Access - Output
    timetable_data_interface.save_ner_annotation_input(timetable_df=df_timetable,
                                                       filepath=path_ner_annotation_input)


if __name__ == '__main__':
    import argparse

    from kronos.nodes.project_logging import default_logging

    default_logging()

    parser = argparse.ArgumentParser(
        description="Collects unique cell text from the timetable "
        "and serialises them for annotation"
    )
    parser.add_argument(
        "-pdt",
        "--path_df_timetable",
        type=Path,
        required=True,
        help="Path from which a serialised timetable dataframe is loaded"
    )
    parser.add_argument(
        "-pnai",
        "--path_ner_annotation_input",
        type=Path,
        required=True,
        help="Path to which NER annotation input is saved"
    )

    args = parser.parse_args()

    save_ner_annotation_input(
        path_df_timetable=args.path_df_timetable,
        path_ner_annotation_input=args.path_ner_annotation_input
    )
