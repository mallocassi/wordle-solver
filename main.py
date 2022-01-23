from heuristics import Heuristics
from state import GameState

SEPARATOR = "\n" + "-".join(["" for idx in range(20)]) + "\n"
ASK_FOR_GUESS = SEPARATOR + "What was your guess?" + SEPARATOR
ASK_FOR_RESULTS = (
    SEPARATOR
    + "What were the results?\n"
    + "Example: 01102\n"
    + "\t- 0 denotes an invalid letter\n"
    + "\t- 1 denotes a misplaced letter\n"
    + "\t- 2 denotes a valid letter"
    + SEPARATOR
)

class WordleSolver:

    def __init__(self, word_list=[], word_length=5, guesses=6):
        print("Wordle Solver")

        self.word_list = word_list
        self.word_list_length = len(word_list)
        self.word_length = word_length
        self.guesses = guesses
        print(f"word_list length: {len(word_list)}")
        print(f"word_length: {word_length}")
        print(f"guesses: {guesses}")

        word_list_letter_count = {}
        for word in word_list:
            idx = 0
            for letter in word:
                letter_count = word_list_letter_count.get(idx, {})
                letter_count[letter] = letter_count.get(letter, 0) + 1
                word_list_letter_count[idx] = letter_count
                idx += 1
        self.word_list_letter_count = word_list_letter_count

        play = True
        while play:
            self.game_state = GameState(word_length=word_length)
            self.game_loop()
            play = input(SEPARATOR+"Play again? (y/n): ").lower() in ["y", "yes"]

        print("Bye")

    def game_loop(self):
        for guess_num in range(self.guesses):
            guess_num = guess_num + 1
            # update game state
            error = True
            while error:
                print(f"\n\nGuessing word {guess_num}")
                # ask for results
                guess = input(ASK_FOR_GUESS).strip().lower()
                results = input(ASK_FOR_RESULTS).replace(" ", "")
                if self.is_win(results):
                    print("Congrats!")
                    return
                try:
                    self.game_state.update(guess, results)
                    error = False
                except IndexError as ex:
                    print(f"\n\nERROR: {ex}")
            # suggest words
            self.suggest_words(guess_num=guess_num)
        print("Woops")

    def is_win(self, results):
        return results == "".join(["2" for i in range(self.word_length)])

    def suggest_words(self, guess_num=1):
        # TODO: check ignore_solution
        possible_words = self.game_state.possible_words(self.word_list, ignore_solution=(guess_num <= 3))
        print(f"\n\nAll possible words: {SEPARATOR}")
        print(", ".join(possible_words))

        score = {}
        for word in possible_words:
            heuristics = Heuristics(word)
            # letter_frequency_score
            heuristics.count_letter_frequency_score(self.word_list_letter_count, self.word_list_length)
            # potential_letters_count
            heuristics.count_potential_letters(self.game_state.potential_letters)
            # potential_letters_count
            heuristics.count_missing_required(self.game_state.solution)
            # bad_letters_count
            heuristics.count_bad_letters(self.game_state.bad_letters)
            # unexplored_letters_count
            heuristics.count_unexplored_letters(self.game_state.unexplored_letters)
            # missing_vowels_count
            heuristics.count_unexplored_vowels(self.game_state.unexplored_letters)
            print(f"Computing score for word: {word}")
            score[word] = heuristics.compute_score(guess_num=guess_num)

        ordered_score = {
            k: v for k, v in sorted(score.items(), key=lambda item: item[1])
        }
        print("\nWords orered by score:" + SEPARATOR)
        for word, score in ordered_score.items():
            print(f"{word}: {score}")


if __name__ == "__main__":
    # Load all words
    word_list = []
    with open("./words.txt", "r") as f:
        for line in f:
            if line not in [None, ""]:
                word_list.append(line.strip())
    WordleSolver(word_list=word_list)
