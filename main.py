import soc
import utils
from icon import Icon
import argparse
import os.path
import os
import fnmatch

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
        self._script = script
    
    def path(self, filename):
        return os.path.join(self._dir, getFullFileName(self._dir, filename))

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
        with open(self._script) as f:
            lines = f.readlines()
        for line in lines:
            args = parseLine(line)
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
        
    
def main():
    parser = argparse.ArgumentParser(description="A script for game automation.")
    parser.add_argument("script", type=str, help="The script file to use")
    args = parser.parse_args()
    app = App(args.script)
    app.run()

if __name__ == '__main__':
    main()