from kronos.nodes.layout_graph import NIDParentToFineGrained, generate_permutations

def test_generate_permutations_standard() -> None:
    data = NIDParentToFineGrained(
        nid_parent=(1, 2),
        nids_fine_grained=[(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    )
    forward_pairs, backward_pairs = generate_permutations(data)
    assert forward_pairs == [((1, 2, 3), (4, 5, 6)), ((4, 5, 6), (7, 8, 9))]
    assert backward_pairs == [((7, 8, 9), (4, 5, 6)), ((4, 5, 6), (1, 2, 3))]

def test_generate_permutations_empty_list() -> None:
    data = NIDParentToFineGrained(
        nid_parent=(1, 2),
        nids_fine_grained=[]
    )
    forward_pairs, backward_pairs = generate_permutations(data)
    assert forward_pairs == []
    assert backward_pairs == []

def test_generate_permutations_single_element_list() -> None:
    data = NIDParentToFineGrained(
        nid_parent=(1, 2),
        nids_fine_grained=[(1, 2, 3)]
    )
    forward_pairs, backward_pairs = generate_permutations(data)
    assert forward_pairs == []
    assert backward_pairs == []