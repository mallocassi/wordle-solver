ALL_LETTERS = [
    letter.lower()
    for letter in [
        "E",
        "A",
        "R",
        "I",
        "O",
        "T",
        "N",
        "S",
        "L",
        "C",
        "U",
        "D",
        "P",
        "M",
        "H",
        "G",
        "B",
        "F",
        "Y",
        "W",
        "K",
        "V",
        "X",
        "Z",
        "J",
        "Q",
    ]
]


class GameState:
    def __init__(self, word_length=5):
        self.word_length = word_length
        self.unexplored_letters = ALL_LETTERS
        self.bad_letters = {idx: [] for idx in range(word_length)}
        self.potential_letters = {idx: [] for idx in range(word_length)}
        self.solution = {idx: [] for idx in range(word_length)}

    def print(self):
        print("Bad letters:")
        print(self.bad_letters)
        print("Potential letters:")
        print(self.potential_letters)
        print("All potential letters:")
        print(self.all_potential_letters())
        print("Solution:")
        print(self.print_solution())

    def print_solution(self):
        solution = ""
        for letter in self.solution.values():
            if letter == []:
                solution += "_"
            else:
                solution += letter
        return solution

    def update(self, guess, results):
        print(f"Updating Game State with guess={guess} and results={results}")
        print("Before update")
        self.print()
        for idx in range(self.word_length):
            try:
                letter = guess[idx]
            except IndexError:
                raise IndexError(f"Entered guess length should be {self.word_length}")
            try:
                result = results[idx]
            except IndexError:
                raise IndexError(f"Entered result length should be {self.word_length}")

            # remove from unexplored letters
            try:
                self.unexplored_letters.remove(letter)
            except ValueError:
                pass

            if result == "0":
                # remove from possible letters
                self.add_bad_letter(letter, idx)
            elif result == "1":
                self.add_potential_letter(letter, idx)
            elif result == "2":
                # add to solution
                self.add_valid_letter(letter, idx)
        self.print()
        input("After update")

    def all_valid_letters(self):
        return filter(lambda x: x not in self.bad_letters, ALL_LETTERS)

    def required_letters(self):
        return list(set([letter for letter in self.solution.values() if letter != []]))

    def unchecked_vowels(self):
        return [
            letter for letter in  ["a", "e", "i", "o", "u", "y"]
            if letter in self.unexplored_letters
        ]

    def possible_words(self, words, ignore_solution=False):
        possible_words = []
        for word in words:
            invalid = False
            if not self.valid_word(word) and not ignore_solution:
                invalid = True
                break
            if not invalid and not ignore_solution:
                for idx, letter in self.solution.items():
                    if letter != [] and word[idx] != letter:
                        invalid = True
                        break
            if not invalid:
                possible_words.append(word)
        return possible_words

    def valid_word(self, word):
        # invalid if bad letters present at each index
        for index, bad_letters in self.bad_letters.items():
            if word[index] in bad_letters:
                return False
        return True

    def add_bad_letter(self, letter, idx):
        self.bad_letters[idx].append(letter)
        self.bad_letters[idx] = list(set(self.bad_letters[idx]))

    def add_potential_letter(self, letter, found_at):
        try:
            self.potential_letters[found_at] = list(set(self.potential_letters[found_at])).remove(letter)
        except ValueError:
            pass
        # add to misplaced letters
        self.add_bad_letter(letter, found_at)

        for idx in range(self.word_length):
            if idx != found_at:
                # only update other indices if not already part of the solution
                if self.solution[idx] == []:
                    self.potential_letters[idx].append(letter)

    def add_valid_letter(self, letter, index):
        self.solution[index] = letter
        self.potential_letters[index] = []

    def all_potential_letters(self):
        all_potential_letters = []
        for _, letters in self.potential_letters.items():
            all_potential_letters.extend(letters)
        for _, letters in self.solution.items():
            all_potential_letters.extend(letters)
        return list(set(all_potential_letters))

    def unexplored_vowels(self):
        return [
            letter for letter in ["a", "e", "i", "o", "u", "y"]
            if letter in self.unexplored_letters
        ]
