from enum import Enum
import random
from typing import Any, Dict, List, Tuple
import networkx as nx
import pandas as pd
import logging

from kronos.nodes.graph_schema import EdgeAttrKey, EdgeType

logger = logging.getLogger(__name__)

class Direction(str, Enum):
    up = "up"
    down = "down"
    left = "left"
    right = "right"

def find_first_non_null(df, start_row, start_col, direction):
    rows, cols = df.shape
    r, c = start_row, start_col

    if direction == Direction.up:
        for i in range(r - 1, -1, -1):
            if pd.notna(df.iloc[i, c]):
                return i, c, r - i  # Distance is r - i
    elif direction == Direction.down:
        for i in range(r + 1, rows):
            if pd.notna(df.iloc[i, c]):
                return i, c, i - r  # Distance is i - r
    elif direction == Direction.left:
        for j in range(c - 1, -1, -1):
            if pd.notna(df.iloc[r, j]):
                return r, j, c - j  # Distance is c - j
    elif direction == Direction.right:
        for j in range(c + 1, cols):
            if pd.notna(df.iloc[r, j]):
                return r, j, j - c  # Distance is j - c
    return None

def df_to_layout_nx_g(df: pd.DataFrame) -> nx.DiGraph:
    nx_g = nx.DiGraph()
    edge_tuples: List[Tuple[int, int, Dict[str, Any]]] = []

    rows, cols = df.shape
    for r in range(rows):
        for c in range(cols):
            if pd.notna(df.iloc[r, c]):
                # Add node with 'raw_text' attribute
                nx_g.add_node((r, c), raw_text=df.iloc[r, c])

                # Check each direction and connect to the first non-null cell
                for direction in Direction:
                    target = find_first_non_null(df, r, c, direction)
                    if target:
                        target_row, target_col, distance = target
                        edge_attrs = {
                            EdgeAttrKey.direction.value: direction.value,
                            EdgeAttrKey.etype.value: EdgeType.layout.value,
                            EdgeAttrKey.distance.value: distance
                        }
                        edge_tuple = ((r, c), (target_row, target_col), edge_attrs)
                        edge_tuples.append(edge_tuple)

    # Add all edges from the prepared list
    nx_g.add_edges_from(edge_tuples)
    
    logger.info(f"Added {len(edge_tuples)} layout edges. Here is an example:\n"
                f"{random.choice(edge_tuples)}")
    
    return nx_g
