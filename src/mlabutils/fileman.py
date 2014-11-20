#!/usr/bin/python
# -*- coding: utf-8 -*-
"""mlabutils.fileman module.

Author: Jan Milík <milikjan@fit.cvut.cz>
"""


import os
import os.path as path
import shutil
import re


class FileEntry(object):
    def __init__(self, directory, rel_path):
        self.directory = directory
        self.rel_path = rel_path

        self.variables = {}
    
    def __repr__(self):
        return "FileEntry(%r, %r)" % (self.directory, self.rel_path, )
    
    @property
    def description(self):
        return "file %s in %s" % (
            self.rel_path,
            self.directory,
        )
    
    def set_var(self, name, value):
        self.variables[str(name)] = value
    
    def iter_dir(self):
        for f in os.listdir(self.abs_path):
            entry = FileEntry(self.directory, path.join(self.rel_path, f))
            yield entry
    
    @property
    def abs_path(self):
        return path.abspath(path.join(self.directory, self.rel_path))

    @property
    def basename(self):
        return path.basename(self.abs_path)

    @property
    def dirname(self):
        return path.dirname(self.abs_path)
    
    @property
    def is_file(self):
        return path.isfile(self.abs_path)
    
    @property
    def is_dir(self):
        return path.isdir(self.abs_path)

    @property
    def mtime(self):
        return datetime.datetime.fromtimestamp(
            os.stat(self.abs_path).st_mtime
        )


class FileEntryStream(object):
    def __init__(self, source, filters = None):
        self.source = source
        self.filters = [] if filters is None else list(filters)

    @property
    def description(self):
        result = self.source.description
        for filter in self.filters:
            result += " " + filter.description
        return result
    
    def filter(self, filter):
        return FileEntryStream(self.source, self.filters + [filter, ])
    
    def __iter__(self):
        for entry in self.source:
            filtered = entry
            for filter in self.filters:
                filtered = filter(filtered)
                if filtered is None:
                    break
            if filtered is None:
                continue
            yield filtered


class FileSource(object):
    def __iter__(self):
        return self.iter_files()
    
    @property
    def description(self):
        return "unknown file source"
    
    def iter_files(self):
        if False:
            yield None
    
    def filter(self, filter):
        return FileEntryStream(self, [filter, ])


class DirectoryFileSource(FileSource):
    def __init__(self, directory, recursive = False):
        FileSource.__init__(self)
        self.directory = directory
        self.recursive = recursive
    
    @property
    def description(self):
        return "files in directory %s" % (path.abspath(self.directory), )
    
    def iter_files(self):
        if not path.isdir(self.directory):
            return
        
        abs_dir = path.abspath(self.directory)
        queue = [FileEntry(abs_dir, "."), ]
        
        while len(queue) > 0:
            current = queue.pop()
            
            for entry in current.iter_dir():
                yield entry
                
                if self.recursive and entry.is_dir:
                    queue.append(entry)
        

class FileFilter(object):
    @property
    def description(self):
        return "unknown file filter"
    
    def __call__(self, entry, *args, **kwargs):
        return self.apply(entry, *args, **kwargs)
    
    def apply(self, entry):
        return entry


class RegExFilter(FileFilter):
    def __init__(self, pattern, set_variables = True):
        FileFilter.__init__(self)
        self.pattern = re.compile(pattern)
        self.set_variables = set_variables
    
    @property
    def description(self):
        return "matching pattern %r" % (self.pattern.pattern, )
    
    def apply(self, entry):
        match = self.pattern.match(entry.basename)
        if match is None:
            return None
        if self.set_variables:
            for name, value in match.groupdict().iteritems():
                entry.set_var(name, value)
        return entry


class IsFileFilter(FileFilter):
    @property
    def description(self):
        return "which are files"
    
    def apply(self, entry):
        if not entry.is_file:
            return None
        return entry


class FormatFilter(FileFilter):
    def __init__(self, format, basename_only = True):
        self.format = format
        self.basename_only = basename_only

    @property
    def description(self):
        return "with name transformed to %r" % (self.format, )
    
    def apply(self, entry):
        variables = dict(entry.variables)
        variables["rel_path"] = path.dirname(entry.rel_path)
        return FileEntry(
            entry.directory,
            self.format.format(**variables)
        )


class OlderThanFilter(FileFilter):
    def __init__(self, ):
        self.descending = descending
    
    def apply(self, entry):
        pass


class FileTask(object):
    def execute(self, files):
        pass


class DeleteTask(FileTask):
    def __init__(self, remove_empty_parents = False):
        FileTask.__init__(self)
    
    def execute(self, files):
        for f in files:
            if f.is_file:
                os.remove(f.abs_path)
            elif f.is_dir:
                shutil.rmtree(f.abs_path)
            try:
                os.removedirs(f.dirname)
            except OSError:
                pass


def main():
    print __doc__


if __name__ == "__main__":
    main()

