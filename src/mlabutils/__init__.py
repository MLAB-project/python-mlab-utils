#!/usr/bin/python
# -*- coding: utf-8 -*-
"""mlabutils module.

Author: Jan Milík <milikjan@fit.cvut.cz>
"""


__version__ = "0.1.2"


import itertools


class IteratorBase(object):
    def next(self):
        raise StopIteration()

    def take_while(self, predicate):
        return IteratorWrapper(itertools.takewhile(predicate, self))


class IteratorWrapper(IteratorBase):
    def __init__(self, iterator, use_stop_element = False, stop_element = None):
        IteratorBase.__init__(self)
        self.iterator = iterator
        self.stop_element = stop_element

    def _next(self):
        if self.use_stop_element:
            try:
                return next(self.iterator)
            except StopIteration:
                return self.stop_element
        else:
            return next(self.iterator)


class BufferedIterator(IteratorWrapper):
    """Wrapper around an iterator which provides buffering and peek operations.
    """

    def __init__(self, iterator, use_stop_element = False, stop_element = None):
        IteratorWrapper.__init__(self, iterator, use_stop_element, stop_element)
        self.buffer = []

    def __iter__(self):
        return self

    def peek(self):
        if len(self.buffer) > 0:
            return self.buffer[0]

        value = next(self.iterator)
        self.buffer.append(value)
        return value

    def peek_list(self, count = 1):
        while len(self.buffer) < count:
            value = next(self.iterator)
            self.buffer.append(value)
        return self.buffer[:count]

    def next(self):
        if len(self.buffer) > 0:
            value = self.buffer[0]
            self.buffer = self.buffer[1:]
            return value
        return next(self.iterator)


def main():
    print(__doc__)


if __name__ == "__main__":
    main()
