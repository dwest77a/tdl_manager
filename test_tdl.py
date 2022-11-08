import pytest

entry_empty = {
    "Format": "", 
    "Description": "", 
    "Type": "", 
    "Dependency": "", 
    "Date": "",
    "rm": False
}

entry_filled = {
    "Format": "test", 
    "Description": "test", 
    "Type": "test", 
    "Dependency": "test", 
    "Date": "test",
    "rm": False
}

entry_rm = {
    "Format": "test", 
    "Description": "test", 
    "Type": "test", 
    "Dependency": "test", 
    "Date": "test",
    "rm": True
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

json_cascade = {
    "0": entry_empty,
    "5": entry_filled,
    "7": entry_empty
}

json_unordered = {
    "3": entry_empty,
    "1": entry_filled,
    "2": entry_empty
}

json_removesched = {
    "0": entry_filled,
    "1": entry_filled,
    "2": entry_rm
}

json_removed = {
    "0": entry_filled,
    "1": entry_filled
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

@pytest.mark.parametrize(
    "json_in, arr_out", [
        (json_unordered, [1,2,3])
    ]
)
def test_gSIK(json_in, arr_out):
    from src.tdlman import getSortedIntKeys

    arr_check = getSortedIntKeys(json_in)
    assert arr_check == arr_out

    return None

@pytest.mark.parametrize(
    "json_in, json_out", [
        (json_cascade, json_base)
    ]
)
def test_cascade(json_in, json_out):
    from src.tdlman import cascade

    json_check = cascade(json_in)
    assert json_check == json_out

    return None

def test_buffer():
    from src.tdlman import buffer

    mystring = 'helloworld'
    bstring = buffer(mystring, 20)
    assert len(bstring) == 20
    assert mystring in bstring

    return None

@pytest.mark.parametrize(
    "json_in, id", [
        (json_base, "0")
    ]
)
def test_removeEntry(json_in, id):
    from src.tdlman import removeEntry

    json_check = removeEntry(json_in, id=id)
    assert json_check[id]['rm'] == True

    return None

@pytest.mark.parametrize(
    "json_in, json_out", [
        (json_removesched, json_removed)
    ]
)
def test_forceRME(json_in, json_out):
    from src.tdlman import forceRemoveEntry
    print(json_in)
    print(json_out)

    json_check = forceRemoveEntry(json_in)
    print(json_check)

    assert json_check == json_out

    return None
