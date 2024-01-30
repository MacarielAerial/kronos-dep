import logging
import random
from enum import Enum
from typing import Any, Dict, List, Tuple, TypedDict

import networkx as nx
from networkx import DiGraph
import pandas as pd

from kronos.nodes.graph_schema import EdgeAttrKey, EdgeType, NodeAttrKey

logger = logging.getLogger(__name__)


class Direction(str, Enum):
    up = "up"
    down = "down"
    left = "left"
    right = "right"


class NIDParentToFineGrained(TypedDict):
    nid_parent: Tuple[int, int]
    nids_fine_grained: List[Tuple[int, int, int]]


def find_first_non_null(  # type: ignore # noqa: C901
    df, start_row, start_col, direction
):
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
    nx_g: nx.DiGraph = nx.DiGraph()
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
                            EdgeAttrKey.distance.value: distance,
                        }
                        edge_tuple = ((r, c), (target_row, target_col), edge_attrs)
                        edge_tuples.append(edge_tuple)  # type: ignore[arg-type]

    # Add all edges from the prepared list
    nx_g.add_edges_from(edge_tuples)

    logger.info(
        f"Added {len(edge_tuples)} layout edges. Here is an example:\n"
        f"{random.choice(edge_tuples)}"
    )

    return nx_g

def derive_nid_parent_to_fined_grained_nid(fine_grained_node_tuples: List[Tuple[Tuple[int, int, int], Dict[str, Any]]]) -> NIDParentToFineGrained:
    nid_parent_to_fine_grained: NIDParentToFineGrained = {}

    for node_tuple in fine_grained_node_tuples:
        # TODO: Explictly declare its schema
        nid = node_tuple[0]
        nid_parent = node_tuple[1][NodeAttrKey.nid_parent.value]
        if nid_parent not in nid_parent_to_fine_grained.keys():
            nid_parent_to_fine_grained.update({nid_parent: [nid]})
        else:
            nid_parent_to_fine_grained[nid_parent].append(nid)
    
    # Sort fine grained node ids based on their last nid tuple element
    for nid_parent, nids_fine_grained in nid_parent_to_fine_grained.items():
        # TODO: Separate the below logic into its own function
        nid_parent_to_fine_grained[nid_parent] = sorted(nid_parent_to_fine_grained[nid_parent_to_fine_grained], key=lambda x: x[0][-1])
    
    return nid_parent_to_fine_grained

# TODO: Stregnthen typing of the return object
def generate_permutations(nid_parent_to_fine_grained: NIDParentToFineGrained) -> Tuple[List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]], List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]]]:
    nids_fine_grained = nid_parent_to_fine_grained['nids_fine_grained']
    n = len(nids_fine_grained)

    # Generate pairs from start to end
    forward_pairs = [(nids_fine_grained[i], nids_fine_grained[i + 1]) for i in range(n - 1)]

    # Generate pairs from end to start
    backward_pairs = [(nids_fine_grained[j + 1], nids_fine_grained[j]) for j in range(n - 2, -1, -1)]

    return forward_pairs, backward_pairs


def derive_fine_grained_edge_tuples(semantics_nx_g: DiGraph, fine_grained_node_tuples: List[Tuple[Tuple[int, int, int], Dict[str, Any]]]) -> List[Tuple[Any, Dict[str, Any]]]:
    # Collect edges inherited from parents first
    inherited_edge_tuples: List[Tuple[int, int, Dict[str, Any]]] = []
    for node_tuple in fine_grained_node_tuples:
        # TODO: Explictly declare this data structure's schema
        nid_fine_grained = node_tuple[0]
        nid_parent = node_tuple[1][NodeAttrKey.nid_parent.value]

        # Find in-edges
        for u, _, d in semantics_nx_g.in_edges(nid_parent, data=True):
            inherieted_in_edge = (u, nid_fine_grained, d)
            inherited_edge_tuples.append(inherieted_in_edge)
        
        # Find out-edges
        for _, v, d in semantics_nx_g.out_edges(nid_parent, data=True):
            inherited_out_edge = (nid_fine_grained, v, d)
            inherited_edge_tuples.append(inherited_out_edge)
    
    # Collect infra-fined-grained-node edges
    infra_fine_grained_edge_tuples: List[Tuple[int, int, Dict[str, Any]]] = []
    nid_parent_to_fine_grained = derive_nid_parent_to_fined_grained_nid(fine_grained_node_tuples)

    # Find edge ids of both directions
    eids_down, eids_up = generate_permutations(nid_parent_to_fine_grained)

    for eid in eids_down + eids_up:
        if eid in eids_down:
            direction = Direction.down.value
        elif eid in eids_up:
            direction = Direction.up.value
        
        infra_edge = (*eid, {EdgeAttrKey.etype.value: EdgeType.layout.value, EdgeAttrKey.direction.value: direction})

        infra_fine_grained_edge_tuples.append(infra_edge)
    
    return inherited_edge_tuples + infra_fine_grained_edge_tuples
