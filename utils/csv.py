import json

utilDef = json.loads("""{
    "type": "db",
    "name": "csv",
    "selftest": 1,
    "requires": [
    ]
}""")

import csv, unittest
import utils.logger

log = utils.logger.register(utilDef['type'])

class Datastore():
    def __init__(self, path):
        self.fullpath = f"utils/util_csv/{path}.csv"
        log(f"Initialising new datastore for {self.fullpath}")

        try:
            target = open(self.fullpath)
        except FileNotFoundError:
            log(f"Unable to locate {self.fullpath}, creating file", 2)
            open(self.fullpath, 'w').close()
            target = open(self.fullpath)

        self.load()

    def exists(self, id):
        return id in self.store

    def read(self, id):
        if self.exists(id):
            return self.store[id]
        else:
            return None

    def update(self, id, payload):
        self.store[id] = payload

    def remove(self, id):
        del self.store[id]

    def save(self):
        log(f"Saving {self.fullpath}")
        target = open(self.fullpath, 'w', newline='')

        writer = csv.DictWriter(
            target, delimiter=',', 
            fieldnames=list(self.store.values())[0].keys(),)

        writer.writeheader()
        writer.writerows(self.store.values())
        target.close()
    
    def load(self):
        target = open(self.fullpath)

        reader = csv.DictReader(target, delimiter=',')
        self.store = {}

        for row in reader:
            self.store[int(row['id'])] = row
        
        target.close()

# Connect to a specific data store
def connect(path):
    return Datastore(path)