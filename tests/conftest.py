import pytest

@pytest.fixture()
def id_ex():
    return "0"

@pytest.fixture()
def reorder_str():
    return "1 0 2"

@pytest.fixture()
def arr_ordered():
    return [1,2,3]

@pytest.fixture()
def entry_mty():
    return {
        "Format": "", 
        "Description": "", 
        "Type": "", 
        "Dependency": "", 
        "Date": "",
        "rm": False
    }

@pytest.fixture()
def entry_filled():
    return {
        "Format": "test", 
        "Description": "test", 
        "Type": "test", 
        "Dependency": "test", 
        "Date": "test",
        "rm": False
    }

@pytest.fixture()
def entry_rm():
    return {
        "Format": "test", 
        "Description": "test", 
        "Type": "test", 
        "Dependency": "test", 
        "Date": "test",
        "rm": True
    }

@pytest.fixture
def json_base(entry_mty, entry_filled):
    return {
        "0": entry_mty,
        "1": entry_filled,
        "2": entry_mty
    }

@pytest.fixture()
def json_reorder(entry_mty, entry_filled):
    return {
        "0": entry_filled,
        "1": entry_mty,
        "2": entry_mty
    }

@pytest.fixture()
def json_cascade(entry_mty, entry_filled):
    return {
        "0": entry_mty,
        "5": entry_filled,
        "7": entry_mty
    }

@pytest.fixture()
def json_unordered(entry_mty, entry_filled):
    return {
        "3": entry_mty,
        "1": entry_filled,
        "2": entry_mty
    }

@pytest.fixture()
def json_remove(entry_mty, entry_filled, entry_rm):
    return {
        "0": entry_mty,
        "1": entry_filled,
        "2": entry_mty,
        "3": entry_rm
    }
