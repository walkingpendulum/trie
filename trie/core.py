from __future__ import annotations

from itertools import chain, islice
from typing import List, Hashable, Dict, Union

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

    def remove_one(self, to_remove: List[Hashable]) -> 'Trie':
        """Remove one element. Input should be a list of tokens (all tokenization work should be already performed)."""
        if not to_remove:
            return self

        subtree = self._tree
        stack = []
        for el, next_el in zip(to_remove, islice(chain(to_remove, [Sentinel]), 1, None)):
            if self.is_sentinel(subtree):
                # special case: {"a": {"b": Sentinel}}, but user requested to delete ["a", "b", "c"]
                raise KeyError(to_remove)

            if el not in subtree:
                raise KeyError(to_remove)

            stack.append(subtree)
            subtree = subtree[el]
            if self.is_sentinel(next_el):
                if not self.is_sentinel(subtree) and "" not in subtree:
                    # special case: {"a": {"b": Sentinel}}, but user requested to delete ["a"]
                    raise KeyError(to_remove)

        if stack[-1][to_remove[-1]] == {"": Sentinel}:
            # special case: after sequence of deletions (i.e. after at least one delete_one)
            # we are in {"a": {"b": {"": Sentinel}}} state, and user requested to delete ["a", "b"]
            # so we normalize state to {"a": {"b": Sentinel}}
            stack[-1][to_remove[-1]] = Sentinel

        for el, subtree in zip(reversed(to_remove), reversed(stack)):
            if self.is_sentinel(subtree[el]):
                del subtree[el]
                continue

            if not subtree[el]:
                del subtree[el]

        return self

    def remove_many(self, many_to_remove: List[List[Hashable]]) -> 'Trie':
        """Remove many elements. Shortcut for multiple remove_one calls."""
        for to_remove in many_to_remove:
            self.remove_one(to_remove)

        return self
