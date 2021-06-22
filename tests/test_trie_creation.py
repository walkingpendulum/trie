from trie.core import Trie, Sentinel


def test_linear_added():
    trie = Trie()
    trie.add_one(["a", "b", "c"])
    assert trie.as_tree() == {"a": {"b": {"c": Sentinel}}}


def test_cherry_added():
    trie = Trie()
    trie.add_one(["root", "cherry1"])
    trie.add_one(["root", "cherry2"])
    assert trie.as_tree() == {"root": {"cherry1": Sentinel, "cherry2": Sentinel}}


def test_add_empty():
    trie = Trie()
    trie.add_one([])
    assert trie.as_tree() == {}


def test_add_many():
    trie = Trie()
    trie.add_many([
        ["mother", "son"],
        ["mother", "daughter"],
    ])
    assert trie.as_tree() == {"mother": {"son": Sentinel, "daughter": Sentinel}}


def test_add_many_with_the_same_prefix_root_level():
    trie = Trie()
    trie.add_many([
        [1],
        [2],
    ])
    assert trie.as_tree() == {1: Sentinel, 2: Sentinel}


def test_add_many_with_the_same_prefix():
    trie = Trie()
    trie.add_many([
        ["grandfather", "father"],
        ["grandfather", "father", "son"],
    ])
    assert trie.as_tree() == {"grandfather": {"father": {"": Sentinel, "son": Sentinel}}}


