import logging
from collections import Counter
from typing import Any, Dict, List, Tuple

import networkx as nx
from networkx import DiGraph
from spacy.language import Language

from kronos.data_interfaces.ner_entities_data_interface import (
    NEREntity,
    list_dict_to_ner_entities,
    list_text_to_list_ner_entities,
)
from kronos.nodes.graph_schema import NodeAttrKey, NodeType

logger = logging.getLogger(__name__)


def augment_nx_g_with_semantics(
    nx_g: nx.DiGraph, spacy_pipeline: Language
) -> nx.DiGraph:
    # Obtain a list of raw texts
    list_raw_text: List[str] = list(
        nx.get_node_attributes(nx_g, NodeAttrKey.raw_text.value).values()
    )

    # Obtain list of lists of NEREntity
    list_ner_entities: List[List[NEREntity]] = list_text_to_list_ner_entities(
        list_raw_text, spacy_pipeline
    )
    list_serialised_ner_entities = [
        [entity.to_dict() for entity in ner_entities]
        for ner_entities in list_ner_entities
    ]

    # Add the new node attribute to the graph
    nx.set_node_attributes(
        G=nx_g,
        values=dict(zip(nx_g.nodes(), list_serialised_ner_entities)),
        name=NodeAttrKey.ner.value,
    )

    logger.info(
        f"Set {NodeAttrKey.ner.value} attribute for "
        f"{len(list_serialised_ner_entities)} nodes in the graph."
    )

    return nx_g

def fine_grained_node_tuples_from_semantics_nx_g(semantics_nx_g: DiGraph) -> List[Tuple[Tuple[int, int, int], Dict[str, Any]]]:
    list_fine_grained_node_tuples: List[Tuple[Tuple[int, int, int], Dict[str, Any]]] = []

    for nid, attrs in semantics_nx_g.nodes.data():
        ner = attrs[NodeAttrKey.ner.value]
        if len(ner) < 1:
            # TODO: Encapsulate node tuple creation logic in a function
            new_nid = tuple(list(nid) + [0])
            ntype = NodeType.other.value
            node_attrs = {NodeAttrKey.ntype.value: ntype,
                          NodeAttrKey.raw_text.value: attrs[NodeAttrKey.raw_text.value]}
            node_tuple = (new_nid, node_attrs)
            list_fine_grained_node_tuples.append(node_tuple)
            continue
        
        ner_ents = list_dict_to_ner_entities(list_dict=ner)

        for i, ner_ent in enumerate(ner_ents):
            ntype = NodeType(ner_ent.label.value).value
            raw_text = ner_ent.text

            # Assemble fine grained node tuple
            new_nid = tuple(list(nid) + [i])  # nid is (x, y) coordinates of a dataframe
            node_attrs = {NodeAttrKey.ntype.value: ntype, 
                          NodeAttrKey.raw_text.value: raw_text,
                          NodeAttrKey.nid_parent.value: nid}
            node_tuple = (new_nid, node_attrs)

            list_fine_grained_node_tuples.append(node_tuple)
    
    logger.info(f"{len(list_fine_grained_node_tuples)} fine grained node tuples "
                "are parsed from NER output")

    return list_fine_grained_node_tuples
