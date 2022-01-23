import math

class Heuristics:

    HEURISTIC_WEIGHTS = {
        "missing_required_letter_count": -1,
        "potential_letters_count": 1,
        "unexplored_letters_count": 2,
        "unexplored_vowels_count": 10,
        "letter_frequency_score": 10,
        "bad_letters_count": -2,
    }

    HEURISTIC_MULTIPLIER = {
        # gets more important with number of guesses made
        "missing_required_letter_count": lambda x: math.exp(x - 2),
        "potential_letters_count": lambda x: math.exp(x),
        "bad_letters_count": lambda x: math.exp(x - 2),
        # gets less important with number of guesses made
        "unexplored_vowels_count": lambda x: math.exp(2 - x),
        # slowly increase in importance
        "letter_frequency_score": lambda x: math.sqrt(x),
        # fixed importance
        "unexplored_letters_count":  lambda x: 10,
    }

    def __init__(self, word):
        self.word = word
        self.heuristics = {
            "missing_required_letter_count": 0,
            "potential_letters_count": 0,
            "bad_letters_count": 0,
            "unexplored_vowels_count": 0,
            "letter_frequency_score": 0,
            "unexplored_letters_count": 0,
        }

    def count_missing_required(self, required_letters_by_index):
        for idx, required_letter in required_letters_by_index.items():
            if self.word[idx] != required_letter:
                self.heuristics["missing_required_letter_count"] += 1

    def count_potential_letters(self, potential_letters_by_index):
        for idx, potential_letters in potential_letters_by_index.items():
            if self.word[idx] in potential_letters:
                self.heuristics["potential_letters_count"] += 1

    def count_bad_letters(self, bad_letters_by_index):
        for idx, bad_letters in bad_letters_by_index.items():
            if self.word[idx] in bad_letters:
                self.heuristics["bad_letters_count"] += 1

    def count_unexplored_letters(self, unexplored_letters):
        seen_letters = []
        for letter in self.word:
            if letter in unexplored_letters and letter not in seen_letters:
                self.heuristics["unexplored_letters_count"] += 1
            # do not double count unexplored letters
            seen_letters.append(letter)

    def count_unexplored_vowels(self, unexplored_letters):
        unexplored_vowels = [
            letter for letter in ["a", "e", "i", "o", "u", "y"]
            if letter in unexplored_letters
        ]
        seen_vowels = []
        for letter in self.word:
            if letter in unexplored_vowels and letter not in seen_vowels:
                self.heuristics["unexplored_vowels_count"] += 1
            # do not double count missing vowels
            seen_vowels.append(letter)

    def count_letter_frequency_score(self, word_list_letter_count, word_list_length):
        for idx, letter in enumerate(self.word):
            base_letter_count = word_list_letter_count[idx][letter]
            # for a given index, the total number of letters is equivalent
            # to the total number of words
            self.heuristics["letter_frequency_score"] += base_letter_count / word_list_length
        self.heuristics["letter_frequency_score"] = self.heuristics["letter_frequency_score"] / len(self.word)

    def compute_score(self, guess_num=0):
        score = 0
        for heur, value in self.heuristics.items():
            multiplier_func = self.HEURISTIC_MULTIPLIER.get(heur, lambda x: 1)
            weight = multiplier_func(guess_num) * self.HEURISTIC_WEIGHTS.get(heur, 1)
            print(f"{heur}: {weight} * {value} = {weight * value}")
            score += weight * value
        return score
