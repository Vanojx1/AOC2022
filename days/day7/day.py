import re
from typing import Union
from termcolor import colored

def singleton(cls):
    classInstances = {}
    def getInstance(name, parent=None):
        key = (name, parent.path if parent else None)
        if key not in classInstances:
            classInstances[key] = cls(name, parent)
        return classInstances[key]
    return getInstance

class File(object):
    def __init__(self, name, size, folder) -> None:
        self.name = name
        self.size = int(size)
        self.folder = folder

    def print(self):
        print('\t' * (self.folder.lvl + 1) + ' - ' + self.__repr__())

    def __hash__(self) -> int:
        return hash((self.name))

    def __repr__(self) -> str:
        return f'{colored(self.name, "green")} (file, size={self.size})'

@singleton
class Folder(object):

    def __init__(self, name, parent=None) -> None:
        self.name = name
        self.content = set()
        self.parent = parent
        self.lvl = parent.lvl + 1 if parent else 0
    
    def add_content(self, el: Union[File, 'Folder']):
        self.content.add(el)
    
    @property
    def path(self):
        if not self.parent: return self.name
        return f'{self.parent.path}/{self.name}'

    @property
    def size(self):
        return sum(map(lambda el: el.size, self.content))
    
    def print(self):
        print('\t' * (self.lvl) + ' - ' + self.__repr__())
        for el in self.content: el.print()
    
    def __hash__(self) -> int:
        return hash((self.name))

    def __repr__(self) -> str:
        return f'{colored(self.name, "green")} (folder, size={self.size})'

CMD_CD = 'CMD_CD'
CMD_PREV = 'CMD_PREV'
CMD_LS = 'CMD_LS'
CMD_FILE = 'CMD_CONTENT'
CMD_DIR = 'CMD_DIR'

def get_command(cmd):
    m = re.match(r'^\$ cd \.\.$', cmd)
    if m: return CMD_PREV, None, None
    m = re.match(r'^\$ cd (\/|\w+)$', cmd)
    if m: return CMD_CD, m.group(1), None
    m = re.match(r'^\$ ls$', cmd)
    if m: return CMD_LS, None, None
    m = re.match(r'^(\d+) (\w+(?:.\w+)?)$', cmd)
    if m: return CMD_FILE, m.group(1), m.group(2)
    m = re.match(r'^dir (\w+)$', cmd)
    if m: return CMD_DIR, m.group(1), None

def main(day_input):

    current = None

    for row in day_input:
        cmd, p1, p2 = get_command(row)

        if cmd == CMD_PREV:
            current = current.parent
        elif cmd == CMD_CD:
            if not current:
                current = Folder(p1)
                continue
            f = Folder(p1, current)
            current.add_content(f)
            current = f
        elif cmd == CMD_FILE:
            f = File(p2, p1, current)
            current.add_content(f)
        elif cmd == CMD_DIR:
            f = Folder(p1, current)
            current.add_content(f)

    # print('\nFilesystem:')
    # Folder('/').print()
    # print()

    folder_type = type(Folder('/'))
    unused_space = 70000000 - Folder('/').size
    req_space = 30000000 - unused_space
    
    def list_dir(curr):
        yield (curr.name, curr.size)
        for el in curr.content:
            if isinstance(el, folder_type):
                yield from list_dir(el)

    smallest_to_delete = None
    total_size = 0
    for _, size in sorted(list_dir(Folder('/')), key=lambda args: args[1]):
        if smallest_to_delete is None and size >= req_space:
            smallest_to_delete = size
        if size <= 100000:
            total_size += size

    return total_size, smallest_to_delete