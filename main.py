import soc
import utils
from icon import Icon
import argparse
import os.path
import os
import fnmatch
import re

def parseLine(line):
    args = line.strip().split()
    return args

def getFullFileName(dir, filename):
    for fn in os.listdir(dir):
        if fnmatch.fnmatch(fn, f'{filename}.*') and os.path.isfile(os.path.join(dir, fn)):
            return fn

class App:
    def __init__(self, script) -> None:
        self._dir = 'soc/img'
        with open(script) as f:
            self._script = [parseLine(line) for line in f]
        self._i = 0
        self._labels = {}
        self._var = {}
    
    def parseArg(self, arg):
        if arg.startswith('$'):
            return self._var[arg]
        if arg.isdecimal():
            return int(arg)
        return arg
    
    def executeLine(self):
        if self._i >= len(self._script):
            return False
        args = self._script[self._i]
        command = args[0]
        if command == 'dir':
            self.dir(args)
        elif command == 'move':
            self.move(args)
        elif command == 'click':
            self.click(args)
        elif command == 'swipeLeft':
            self.swipeLeft(args)
        elif command == 'swipeRight':
            self.swipeRight(args)
        elif command == 'clear':
            self.clear()
        elif command == 'wait':
            self.wait(args)
        elif command == 'any':
            self.any(args)
        elif command == 'label':
            self._labels[args[1]] = self._i
        elif command == 'goto':
            self.goto(args[1])
        elif command == 'var':
            var_name = args[1]
            var_value = args[2]
            self._var[var_name] = self.parseArg(var_value)
        elif command == 'lt':
            arg1 = self.parseArg(args[1])
            arg2 = self.parseArg(args[2])
            if arg1 < arg2:
                self.goto(args[3])
        elif command == 'le':
            arg1 = self.parseArg(args[1])
            arg2 = self.parseArg(args[2])
            if arg1 <= arg2:
                self.goto(args[3])
        elif command == 'add':
            arg1 = self.parseArg(args[1])
            arg2 = self.parseArg(args[2])
            self._var[args[3]] = arg1 + arg2
        
        return True
    
    def path(self, filename):
        return os.path.join(self._dir, getFullFileName(self._dir, filename))
    
    def goto(self, label):
        self._i = self._labels[label]

    def dir(self, args):
        self._dir = args[1]
    
    def move(self, args):
        icon = Icon.create(self.path(args[1]))
        icon.hover()
    
    def click(self, args):
        icon = Icon.create(self.path(args[1]))
        icon.click()
    
    def swipeLeft(self, args):
        icon = Icon.create(self.path(args[1]))
        icon.swipeLeft()
        
    def swipeRight(self, args):
        icon = Icon.create(self.path(args[1]))
        icon.swipeRight()

    def wait(self, args):
        for arg in args:
            icon = Icon.create(self.path(args[1])) 
            icon.locate()

    def any(self, args):
        raise NotImplementedError()
    
    def clear(self):
        Icon.pool.clear()

    def run(self):
        while self.executeLine():
            self._i += 1
        
    
def main():
    parser = argparse.ArgumentParser(description="A script for game automation.")
    parser.add_argument("script", type=str, help="The script file to use")
    args = parser.parse_args()
    app = App(args.script)
    app.run()

if __name__ == '__main__':
    main()