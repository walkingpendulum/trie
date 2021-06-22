from __future__ import annotations

from itertools import chain, islice
from typing import List, Hashable, Dict, Union, cast

TreeType = Union['TreeType', Dict[Hashable, 'TreeType']]


class Sentinel:
    pass


class Trie(object):
    """Implements prefix tree data structure (see https://en.wikipedia.org/wiki/Trie)"""
    def __init__(self):
        self._tree = {}

    def add_one(self, to_add: List[Hashable]) -> 'Trie':
        """Add one element. Input should be a list of tokens (all tokenization work should be already performed)."""
        if not to_add:
            return self

        prev_subtree, subtree = None, self._tree
        it = zip(chain([Sentinel], to_add), to_add, islice(chain(to_add, [Sentinel]), 1, None))
        for prev_el, el, next_el in it:
            if self.is_sentinel(next_el):
                # this is the last element to add
                if self.is_sentinel(subtree):
                    # this is a special case: add_one(["a"]), then add_one(["a", "b]); and el == "b" right now
                    # lets patch subtree to be {"": Sentinel} first
                    subtree = {"": Sentinel}
                    prev_subtree[prev_el] = subtree      # prev_subtree is always not None here!     # noqa

                subtree[el] = Sentinel
                break

            if el not in subtree:
                subtree[el] = {}

            prev_subtree, subtree = subtree, subtree[el]

        return self

    def add_many(self, many_to_add: List[List[Hashable]]) -> 'Trie':
        """Add many elements. Shortcut for multiple add_one calls."""
        for to_add in many_to_add:
            self.add_one(to_add)

        return self

    def as_tree(self) -> TreeType:
        return self._tree

    def is_sentinel(self, obj) -> bool:
        return obj == Sentinel
