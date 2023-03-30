
import sys

class Argv():

    ARGV = sys.argv
    INSTANCE = None

    def __init__(self):
        self._argv = Argv.ARGV
        self.container = {}
        self._build()
    
    def _build(self):
        for index, arg in enumerate(self._argv):
            if '=' in arg:
                key, value = arg.split('=')
                self.container[key] = value
            self.container[index] = arg

    @staticmethod
    def _instance():
        if Argv.INSTANCE is not None:
            return Argv.INSTANCE
        Argv.INSTANCE = Argv()
        return Argv.INSTANCE

    @staticmethod
    def get(key, default=None):
        inst = Argv._instance()
        return inst.container.get(key,default)
    
    @staticmethod
    def container():
        inst = Argv._instance()
        return inst.container