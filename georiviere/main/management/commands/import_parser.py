from importlib import import_module

# We can't use normal importation because the filename is import in Geotrek which is an instruction
Command = import_module('geotrek.common.management.commands.import').Command
