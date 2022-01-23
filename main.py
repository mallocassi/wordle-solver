import math

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

HEURISTIC_WEIGHTS = {
    "all_potential_letters_count": 2,
    "unexplored_letters_count": 2,
    "missing_vowels_count": 2,
    "letter_frequency": 100,
    "is_missing_potential_letters": -1,
    "is_missing_required_letters": -2,
    "has_bad_letters": -2,
}

HEURISTIC_MULTIPLIER = {
    "is_missing_required_letters": lambda x: math.exp(x - 2),
    "has_bad_letters": lambda x: math.exp(x - 2),
    "unexplored_letters_count":  lambda x: 10,
    "is_missing_potential_letters": lambda x: math.exp(x),
    "missing_vowels_count": lambda x: math.exp(2 - x),
    "letter_frequency": lambda x: math.sqrt(x),
}

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
            # update game state
            error = True
            while error:
                print(f"\n\nGuessing word {guess_num+1}")
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
            self.suggest_words(guess_num=guess_num+1)
        print("Woops")

    def is_win(self, results):
        return results == "".join(["2" for i in range(self.word_length)])

    def suggest_words(self, guess_num=0):
        # TODO: use guess_num to adapt strategy?

        possible_words = self.game_state.possible_words(self.word_list, ignore_solution=(guess_num <= 3))
        print(f"\n\nAll possible words: {SEPARATOR}")
        print(", ".join(possible_words))

        score = {}
        potential_letters = self.game_state.all_potential_letters()
        for word in possible_words:
            heuristics = {
                "all_potential_letters_count": 0,
                "unexplored_letters_count": 0,
                "letter_frequency": 0,
                "missing_vowels_count": 0,
                "is_missing_potential_letters": False,
                "is_missing_required_letters": False,
                "has_bad_letters": False,
            }

            # TODO: Refactor

            # is_missing_potential_letters
            for potential_letter in potential_letters:
                if potential_letter not in word:
                    heuristics["is_missing_potential_letters"] = True
                    break

            # is_missing_required_letters
            for required_letter in self.game_state.required_letters():
                if required_letter not in word:
                    heuristics["is_missing_required_letters"] = True
                    break

            # missing_vowels
            missing_vowels = [
                letter for letter in ["a", "e", "i", "o", "u", "y"]
                if letter in self.game_state.unexplored_letters
            ]

            checked_letters = {}
            for idx, letter in enumerate(word):

                # missing_vowels_count
                if letter in missing_vowels:
                    heuristics["missing_vowels_count"] += 1
                    # don't double count missing vowels
                    try:
                        missing_vowels.remove(letter)
                    except:
                        pass

                # all_potential_letters_count
                if letter in self.game_state.bad_letters.get(idx, []):
                    heuristics["has_bad_letters"] = True

                # all_potential_letters_count
                if letter in potential_letters:
                    heuristics["all_potential_letters_count"] += 1

                # unexplored_letters_count
                if letter in self.game_state.unexplored_letters \
                and not checked_letters.get(letter, False):
                    heuristics["unexplored_letters_count"] += 1
                    # do not double count unexplored letters
                    checked_letters[letter] = True

                # letter_frequency
                # for a given index, the total number of letters is equivalent
                # to the total number of words
                letter_count = self.word_list_letter_count[idx][letter]
                heuristics["letter_frequency"] += letter_count / self.word_list_length

            heuristics["letter_frequency"] = heuristics["letter_frequency"] / self.word_length
            print(f"Computing score for word: {word}")
            score[word] = self.compute_score(heuristics, guess_num=guess_num)

        ordered_score = {
            k: v for k, v in sorted(score.items(), key=lambda item: item[1])
        }
        print("\nWords orered by score:" + SEPARATOR)
        for word, score in ordered_score.items():
            print(f"{word}: {score}")

    def compute_score(self, heuristics, guess_num=1):
        score = 0
        for heur, value in heuristics.items():
            multiplier_func = HEURISTIC_MULTIPLIER.get(heur, lambda x: 1)
            weight = multiplier_func(guess_num) * HEURISTIC_WEIGHTS.get(heur, 1)
            print(f"{heur}: {weight} * {value} = {weight * value}")
            score += weight * value
        return score


if __name__ == "__main__":
    # Load all words
    word_list = []
    with open("./words.txt", "r") as f:
        for line in f:
            if line not in [None, ""]:
                word_list.append(line.strip())
    WordleSolver(word_list=word_list)
