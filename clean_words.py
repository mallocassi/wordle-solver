word_list = []
with open("./words.txt", "r") as f:
    for line in f:
        if line not in word_list:
            word_list.append(line)
word_list.sort()
with open("./words.txt", "w") as f:
    f.writelines(word_list)
