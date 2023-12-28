import networkx as nx
import pandas as pd


def df_to_layout_nx_g(df: pd.DataFrame) -> nx.Graph:
    """
    Creates a network from a DataFrame, where each non-null cell is a node.
    Edges are added based on non-null cell proximity (up, down, left, right).
    Cell values are preserved in a node attribute 'raw_text'.
    Edge directions are preserved as edge attributes.

    :param df: DataFrame representing the table.
    :return: A NetworkX Graph object.
    """
    G: nx.Graph = nx.Graph()

    rows, cols = df.shape
    for r in range(rows):
        for c in range(cols):
            if pd.notna(df.iloc[r, c]):
                # Add node with 'raw_text' attribute
                G.add_node((r, c), raw_text=df.iloc[r, c])

                # Add edges with direction attributes
                # Left
                if c > 0 and pd.notna(df.iloc[r, c - 1]):
                    G.add_edge((r, c), (r, c - 1), direction="left")
                # Right
                if c < cols - 1 and pd.notna(df.iloc[r, c + 1]):
                    G.add_edge((r, c), (r, c + 1), direction="right")
                # Up
                if r > 0 and pd.notna(df.iloc[r - 1, c]):
                    G.add_edge((r, c), (r - 1, c), direction="up")
                # Down
                if r < rows - 1 and pd.notna(df.iloc[r + 1, c]):
                    G.add_edge((r, c), (r + 1, c), direction="down")

    return G
