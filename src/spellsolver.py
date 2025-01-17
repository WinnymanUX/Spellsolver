from src.modules.resultlist import ResultList, ResultWord
from src.modules.gameboard import GameBoard
from src.modules.validate import WordValidate
from src.modules.trie import TrieNode
from src.modules.path import Path
from src.utils import Timer


class SpellSolver:
    """Solve a Spellcast game"""
    def __init__(self, validate: WordValidate, gameboard: GameBoard) -> None:
        self.gameboard: GameBoard = gameboard
        self.validate: WordValidate = validate

    def process_node(self, node: TrieNode, actual_word: str, actual_path: Path, swap: bool) -> list[ResultWord]:
        """Recursively process a node to find posible valid words"""
        paths = []
        for word in node.get_leaf(key="word0"):
            paths += [ResultWord(points=actual_path.word_points(), word=word, path=actual_path.path_tuple())]

        if swap:
            for word in node.get_leaf(key="word1"):
                # Gets the index of the letter that is in word but not in actual_word
                index = next((i for i in range(len(actual_word)) if word[i]!=actual_word[i]), len(actual_word))
                
                for path in actual_path.complete_path(self.gameboard.tiles, word, index):
                    paths += [ResultWord(points=path.word_points(), word=word, path=path.path_tuple(), swap=index)]
        return paths

    def posible_paths(self, word: str, path: Path, swap: bool) -> list[ResultWord]:
        """Get all posible paths that complete a path using swap"""
        paths = []
        for neighbor in path.suggest_node(path.path[-1].neighbors):
            actual_word = word + neighbor.letter
            actual_path = Path(path.path + [neighbor])

            node = self.validate.trie.get_node(actual_word)
            if node:
                paths += self.process_node(node, actual_word, actual_path, swap)
                paths += self.posible_paths(actual_word, actual_path, swap)
        return paths

    def word_list(self, swap: bool=True, timer: Timer=None) -> ResultList:
        """Get a valid words list from a solver Spellcast game"""
        results = ResultList(timer=timer)
        for tile in self.gameboard.tiles.values():
            paths = self.posible_paths(word="", path=Path([tile]), swap=swap)
            results.update(paths)
        return results


if __name__ == "__main__":
    gameboard = GameBoard()
    validate = WordValidate()
    validate.load_file("wordlist/wordlist_english.txt")

    while(True):
        gameboard_string = input("Insert a gameboard: ")
        gameboard.load(gameboard_string)
        spellsolver = SpellSolver(validate, gameboard)

        swap = input("Use swap?: ") != "0"
        spellsolver.word_list(swap=swap)
