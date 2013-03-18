import os
from tables import *

class FileSystem(IsDescription):
    label      = StringCol(16, pos=1)   # 16-character String
    path       = StringCol(16, pos=2)   # 16-character String
    name       = StringCol(16, pos=3)   # 16-character String
    size       = Int32Col(pos=4)      # integer
    time       = Int32Col(pos=5)      # integer
    hash       = StringCol(16, pos=6)   # 16-character String
    checked    = UInt8Col(pos=7)      # unsigned byte

class Hd5():
    def __init__(self, **kwargs):
        self.edited = False
        self.index = {}

        if 'filename' in kwargs and kwargs['filename']:
            self.filename = kwargs['filename']
        else:
            self.filename = 'files.hd5'

        if os.path.exists(self.filename):
            self.db = openFile(self.filename, mode="r+")
            self.group = self.db.root.group
            self.table = self.db.root.group.table
            self.index = {r['label']:r.nrow for r in self.table.iterrows()}
        else:
            self.db = openFile(self.filename, mode = "w", title = "Test file")
            self.group = self.db.createGroup("/", 'group', 'Detector information')
            self.table = self.db.createTable(self.group, 'table', FileSystem, "Readout example")
            self.db.flush()

    def set(self, k, l):
        row = self.table.row
        row['label']  = l[0]
        row['path'] = l[1]
        row['name'] = l[2]
        row['size'] = l[3]
        row['time'] = l[4]
        row['hash'] = l[5]
        row['checked'] = l[6]
        row.append()
        self.table.flush()

        self.index[l[0]] = row.nrow

        self.edited = True

    def get(self, k):
        return self.table[self.index[k]]

    def exists(self, k):
        return k in self.index

    def values(self):
        return self.table.iterrows()

    def delete(self, k):
        self.edited = True
        #del self.db[k]
        return #

    def iteritems(self):
        return #self.db.iteritems()

    def sync(self):
        if self.edited:
            self.table.flush()

    def close(self):
        self.db.close()
