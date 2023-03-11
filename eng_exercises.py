import random
import pandas as pd

df = pd.read_csv("dictionary.csv", header=None, sep=";", encoding="cp1250", index_col=0).squeeze(axis=1)
dict_of_words = df.to_dict()


def eng_pol(number_of_words=0):
    if number_of_words == 1:
        eng_word = random.choice(list(dict_of_words))
        pol_word = dict_of_words[eng_word]
        print(eng_word, end=" - ")
        if input():
            print(pol_word.upper(), end="\n\n")
    else:
        while True:
            eng_word = random.choice(list(dict_of_words))
            pol_word = dict_of_words[eng_word]
            print(eng_word, end=" - ")
            if input():
                print(pol_word.upper(), end="\n\n")


def pol_eng(number_of_words=0):
    if number_of_words == 1:
        eng_word = random.choice(list(dict_of_words))
        pol_word = dict_of_words[eng_word]
        print(pol_word, end=" - ")
        if input():
            print(eng_word.upper(), end="\n\n")
    else:
        while True:
            eng_word = random.choice(list(dict_of_words))
            pol_word = dict_of_words[eng_word]
            print(pol_word, end=" - ")
            if input():
                print(eng_word.upper(), end="\n\n")


def random_choice():
    while True:
        if random.randint(0, 1) == 0:
            eng_pol(1)
        else:
            pol_eng(1)


if __name__ == "__main__":
    random_choice()