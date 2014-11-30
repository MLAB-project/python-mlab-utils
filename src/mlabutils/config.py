#!/usr/bin/python
# -*- coding: utf-8 -*-
"""mlabutils.config module.

.. attribute:: DEFAULT_BUILDER

    Default :class:`Builder` instance used by some of the functions in this module.

"""


import logging

from mlabutils import ejson
from mlabutils.utils import obj_repr, getClassLogger


class Builder(object):
    """Builder processes a data structure made of various python data types
    (lists, dictionaries, integers, strings, etc.), possibly loaded from
    a config file, and uses it instantiate application objects.
    """

    FACTORY_KEYS = ("type", "factory", )

    def __init__(self):
        self.factories = {}

        self.logger = getClassLogger(self)

    def add_factory(self, name, factory):
        self.factories[str(name)] = factory
        return factory

    def build(self, config):
        """Builds application objects from configuration data.
        """

        if isinstance(config, list):
            result = []

            for item in config:
                result.append(self.build(item))

            return result

        if isinstance(config, dict):
            # Create new dictionary with processed values
            new_dict = {}
            for key, value in config.iteritems():
                new_dict[key] = self.build(value)

            # Get factory name
            factory_name = None
            for factory_name_key in self.FACTORY_KEYS:
                factory_name = config.get(factory_name_key, None)
            # If the dict doesn't have a factory name,
            # just return the dict itself.
            if factory_name is None:
                return new_dict

            # Get the factory itself
            factory = self.factories.get(factory_name, None)
            if factory is None:

                factory = FactoryDummy(factory_name)

            # Create the instance using the selected factory
            return factory(new_dict)

        return config


class FactoryDummy(object):
    def __init__(self, factory_name):
        self._factory_name = factory_name

    def __call__(self, config):
        return DummyObject(self._factory_name, config)


class DummyObject(object):
    def __init__(self, factory_name, config):
        self._factory_name = factory_name
        self._config = config

    def __repr__(self):
        return obj_repr(self, self._factory_name, self._config)

    def __getattr__(self, name):
        try:
            return self._config[name]
        except KeyError:
            raise AttributeError()

    def __pprint__(self, printer, level = 0):
        printer.writeln("DummyObject(")
        printer.indent()
        printer.format_inner(self._factory_name, level + 1)
        printer.writeln(",")
        printer.format_inner(self._config, level + 1)
        printer.unindent()
        printer.writeln()
        printer.write(")")


DEFAULT_BUILDER = Builder()


def add_factory(name, factory):
    return DEFAULT_BUILDER.add_factory(name, factory)


def build(config):
    return DEFAULT_BUILDER.build(config)


def load_file(file_name):
    """Loads and builds configuration from a EJSON file
    using :class:`mlabutils.ejson.Parser` parser and
    :attr:`DEFAULT_BUILDER` builder.
    """
    parser = ejson.Parser()
    config = parser.parse_file(file_name)
    return build(config)


def main():
    print __doc__


if __name__ == "__main__":
    main()

