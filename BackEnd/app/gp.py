from functools import reduce

class Trie:
    def __init__(self):
        self.children = {}
        self.WordEnd = False  # WordEnd to represent that a word ends at this node

    def initialize(self, file):
        with open(file, encoding='utf-8', errors='ignore') as FileObj:  # Reading File
            for word in FileObj:
                self.insert(word[0:-1])

    def insert(self, word):  # Setting Trie (1)
        for char in word:
            if char not in self.children:
                self.children[char] = Trie()
            self = self.children[char]
        self.WordEnd = True

    def all_suffixes(self, prefix):
        results = set()

        if self.WordEnd:
            results.add(prefix)

        if not self.children:
            return results

        return reduce(lambda a, b: a | b, [node.all_suffixes(prefix + char) for (char, node) in self.children.items()])

    def autocomplete(self, prefix):
        node = self
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return list(node.all_suffixes(prefix))

    def predict(self, input_word):
        if len(input_word) >= 3:
            suggested = self.autocomplete(input_word)
            return suggested[0:5]
        return []

