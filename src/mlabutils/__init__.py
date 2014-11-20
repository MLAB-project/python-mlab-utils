#!/usr/bin/python
# -*- coding: utf-8 -*-
"""mlabutils module.

Author: Jan Milík <milikjan@fit.cvut.cz>
"""


__version__ = "0.1~dev"


class BufferedIterator(object):
    def __init__(self, iterator):
        self.iterator = iterator
        self.buffer = []

    def peek(self):
        if len(self.buffer) > 0:
            return self.buffer[0]
        
        value = next(self.iterator)
        self.buffer.append(value)
        return value
    
    def __next__(self):
        if len(self.buffer) > 0:
            value = buffer[0]
            self.buffer = self.buffer[1:]
            return value
        return next(self.iterator)


def main():
    print __doc__


if __name__ == "__main__":
    main()

