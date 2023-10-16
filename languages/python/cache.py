import os
import pickle

class Cache:
    def __init__(self, path):
        self.path = path
        self.dict = {}
        self.saved = False
        if os.path.exists(path):
            with open(path, 'rb') as f:
                self.dict = pickle.load(f)
            self.saved = True

    def __bool__(self):
        if not self.dict:
            # need to build cache
            return True
        else:
            # cache hit
            return False

    def __setitem__(self, key, value):
        self.saved = False
        self.dict[key] = value

    def __getitem__(self, key):
        if not self.saved:
            self.save()
        return self.dict[key]

    def get(self, key, default=None):
        return self.dict.get(key, default)

    def save(self):
        with open(self.path, 'wb') as f:
            pickle.dump(self.dict, f)
        self.saved = True
