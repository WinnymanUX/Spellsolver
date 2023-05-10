from trie import TrieLeaf, TrieNode
from utils import Timer


class ValidateLeaf(TrieLeaf):
    def __init__(self):
        self.words = {}

    def insert(self, **kwargs: dict):
        for key, value in kwargs.items():
            self.words.setdefault(key, []).append(value)
    
    def get(self, key: str):
        return self.words.get(key, [])

class WordValidate:
    def __init__(self):
        self.trie: TrieNode = TrieNode('', ValidateLeaf)
        self.timer: Timer = Timer()

    def word0(self, word: str):
        self.trie.insert(word, word0=word)

    def word1(self, word: str):
        for pos in range(len(word)):
            iword = word[:pos] + word[pos+1:]
            self.trie.insert(iword, word1=word)

    def load_file(self, path):
        print("WordValidate is being initialized, this will take several seconds")
        self.timer.reset_timer()
        with open(path) as file:
            for word in file.readlines():
                word = word[:-1]
                self.word1(word)
                self.word0(word)
        print(f"WordValidate successfully initialized (elapsed time: {self.timer.elapsed_seconds()} seconds)")

        
if __name__ == "__main__":
    validate = WordValidate()
    validate.load_file("wordlist/wordlist_english.txt")

    def node_str(node: TrieNode):
        return f"word0: {node.get_words('word0', recursive=True)}\nword1: {node.get_words('word1', recursive=True)}\n"

    while(True):
        word = input("Insert a word: ")
        node = validate.trie.get_node(word)
        print(node_str(node) if node else f"There are no word started in {word}")
