import logging
import os
import yaml


class Exporter(object):
    """Helper class for dumping data into filesystem."""

    def __init__(self, path: str) -> object:
        """
        :param path: path of root directory to receive dumps
        """
        self.root = path

    def dump(self, ctx: str, data: list) -> None:
        """Dump a Netbox dataset to disk in YAML syntax.
        
        :param ctx:     data's context (section)
        :param data:    payload dataset
        """
        if not os.path.exists(self.root):
            os.mkdir(self.root)
        dirname, basename = ctx.split(os.path.sep)
        parent = os.path.join(self.root, dirname)
        if not os.path.exists(parent):
            os.mkdir(parent)
        path = os.path.join(parent, basename)
        with open(path, "w") as dumpfile:
            dumpfile.write(yaml.dump(data))

