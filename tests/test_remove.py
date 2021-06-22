import pytest

from trie.core import Trie, Sentinel


def test_remove_absent_root():
    trie = Trie()
    trie.add_one(["a"])
    with pytest.raises(KeyError) as cm:
        trie.remove_one(["b"])

    assert KeyError == cm.type
    assert ["b"] == cm.value.args[0]


def test_remove_absent():
    trie = Trie()
    trie.add_one(["a", "b"])
    with pytest.raises(KeyError) as cm:
        trie.remove_one(["a", "c"])

    assert KeyError == cm.type
    assert ["a", "c"] == cm.value.args[0]


def test_remove_absent_with_subword_short():
    trie = Trie()
    trie.add_one(["a", "b", "c"])
    with pytest.raises(KeyError) as cm:
        trie.remove_one(["a", "b"])

    assert KeyError == cm.type
    assert ["a", "b"] == cm.value.args[0]


def test_remove_absent_with_subword_long():
    trie = Trie()
    trie.add_one(["a", "b"])
    with pytest.raises(KeyError) as cm:
        trie.remove_one(["a", "b", "c"])

    assert KeyError == cm.type
    assert ["a", "b", "c"] == cm.value.args[0]


def test_remove_cherry_small_partially():
    trie = Trie()

    trie.add_many([
        ["root", "cherry1"],
        ["root", "cherry2"],
    ])
    trie.remove_one(["root", "cherry2"])
    assert trie.as_tree() == {"root": {"cherry1": Sentinel}}


def test_remove_cherry_small_whole():
    trie = Trie()

    trie.add_many([
        ["root", "cherry1"],
        ["root", "cherry2"],
    ])
    trie.remove_one(["root", "cherry1"])
    trie.remove_one(["root", "cherry2"])
    assert trie.as_tree() == {}


def test_remove_cherry_big():
    trie = Trie()

    trie.add_many([
        ["root", "branch1"],
        ["root", "branch1", "cherry1"],
        ["root", "branch2", "cherry21"],
        ["root", "branch2", "cherry22"],
    ])
    trie.remove_one(["root", "branch1", "cherry1"])
    trie.remove_one(["root", "branch2", "cherry21"])
    trie.remove_one(["root", "branch2", "cherry22"])

    tree = trie.as_tree()
    assert tree == {"root": {"branch1": Sentinel}} or tree == {"root": {"branch1": {"": Sentinel}}}


def test_remove_from_linearized():
    trie = Trie()

    trie.add_many([
        ["grandfather"],
        ["grandfather", "father"],
    ])
    trie.remove_one(["grandfather", "father"])
    tree = trie.as_tree()
    assert tree == {"grandfather": {"": Sentinel}} or tree == {"grandfather": Sentinel}


def test_remove_multiple_from_linearized():
    trie = Trie()

    trie.add_many([
        ["grandfather"],
        ["grandfather", "father"],
        ["grandfather", "father", "son"],
    ])
    trie.remove_one(["grandfather", "father", "son"])
    trie.remove_one(["grandfather", "father"])
    tree = trie.as_tree()
    assert tree == {"grandfather": Sentinel} or tree == {"grandfather": {"": Sentinel}}
