import pytest

def test_reorder(json_reorder, json_base, reorder_str):
    from tdlman.tdlman import reorder

    json_check = reorder(json_reorder, reorder_str=reorder_str)

    assert json_check == json_base


def test_gSIK(json_unordered, arr_ordered):
    from tdlman.tdlman import getSortedIntKeys

    arr_check = getSortedIntKeys(json_unordered)
    assert arr_check == arr_ordered

    return None

def test_cascade(json_cascade, json_base):
    from tdlman.tdlman import cascade

    json_check = cascade(json_cascade)
    assert json_check == json_base

    return None

def test_buffer():
    from tdlman.tdlman import buffer

    mystring = 'helloworld'
    bstring = buffer(mystring, 20)
    assert len(bstring) == 20
    assert mystring in bstring

    return None

def test_removeEntry(json_base, id_ex):
    from tdlman.tdlman import removeEntry

    print(json_base)

    json_check = removeEntry(json_base, id=id_ex)
    assert json_check[id_ex]['rm'] == True

    return None


def test_forceRME(json_remove, json_base):
    from tdlman.tdlman import forceRemoveEntry

    json_check = forceRemoveEntry(json_remove)

    assert json_check == json_base

    return None
