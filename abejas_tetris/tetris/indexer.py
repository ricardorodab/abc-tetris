
indexer = None

def get_index():
    global indexer
    if indexer == None:
        indexer = Indexer()
    return indexer.get_index()

class Indexer():
    def __init__(self):
        self.id = 0

    def get_index(self):
        self.id = self.id + 1
        return self.id