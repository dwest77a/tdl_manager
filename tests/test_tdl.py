import pytest

entry_empty = {
    "Format": "", 
    "Description": "", 
    "Type": "", 
    "Dependency": "", 
    "Date": ""
}

entry_filled = {
    "Format": "test", 
    "Description": "test", 
    "Type": "test", 
    "Dependency": "test", 
    "Date": "test"
}

json_base = {
    "0": entry_empty,
    "1": entry_filled,
    "2": entry_empty
}

json_reorder = {
    "0": entry_filled,
    "1": entry_empty,
    "2": entry_empty
}


@pytest.mark.parametrize(
    "json_in, json_out, reorder_str", [
        (json_base, json_reorder, "1 0 2")
    ]
)
def test_reorder(json_in, json_out, reorder_str):
    from src.tdlman import reorder

    json_check = reorder(json_in, reorder_str=reorder_str)

    assert json_check == json_out
