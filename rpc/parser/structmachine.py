#coding:utf-8
# 2014-12-18
# build by qianqians
# structmachine

from deletenonespacelstrip import deleteNoneSpacelstrip

class elem(object):
    def __init__(self):
        self.keyworld = ''
        self.key = ""
        self.value = None

    def clear(self):
        self.keyworld = ''
        self.key = ""
        self.value = None

    def push(self, ch):
        if ch in [' ', '    ', '\r', '\n', '\t', '\0'] and self.keyworld != '':
            self.keyworld = deleteNoneSpacelstrip(self.keyworld)
            if self.keyworld != '':
                self.key = self.keyworld
            self.keyworld = ''
            return False

        if ch == ';':
            self.keyworld = deleteNoneSpacelstrip(self.keyworld)
            if self.keyworld != '':
                self.value = self.keyworld
            self.keyworld = ''
            return True

        self.keyworld += ch
        self.keyworld = deleteNoneSpacelstrip(self.keyworld)

        return False

class struct(object):
    def __init__(self):
        self.keyworld = ''
        self.name = ''
        self.elem = []
        self.machine = None

    def push(self, ch):
        if ch == '}':
            return True

        if self.machine is not None:
            if self.machine.push(ch):
                self.elem.append((self.machine.key, self.machine.value))
                self.machine.clear()
        else:
            if ch == '{':
                self.keyworld = deleteNoneSpacelstrip(self.keyworld)
                if self.keyworld != '':
                    self.name = deleteNoneSpacelstrip(self.keyworld)
                self.keyworld = ''
                self.machine = elem()
                return False

            self.keyworld += ch

        return False