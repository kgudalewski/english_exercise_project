import random
import pandas as pd
import warnings
import sys
warnings.filterwarnings('ignore')

df = pd.read_csv("dictionary.csv", index_col=0)

print("Hello in English learning app !")
print("-------------------------------")
print("Type 'exit' for correct question to save and exit the game")
print("-------------------------------")
print("Let's start the game !!", end="\n\n")


def sort_df_by_weight():
    global df
    df = df.sort_values(by="weights").reset_index(drop=True)


def check_func(idx):
    global df
    yes_rate = 1.3
    no_rate = 0.7
    answer = input("Correct ? [Y/N] ").upper()
    if answer == "Y":
        df.weights[idx] *= yes_rate
        sort_df_by_weight()
    elif answer == "N":
        df.weights[idx] *= no_rate
        sort_df_by_weight()
    elif answer == "EXIT":
        df.to_csv("dictionary.csv")
        sys.exit()
    print()


def eng_pol(number_of_words=0):

    percent_of_words = 0.2
    if number_of_words == 1:
        idx = random.randint(0, int(round(df.shape[0] * percent_of_words)))
        eng_word = df.ANG[idx]
        pol_word = df.POL[idx]
        print(eng_word, end=" - ")
        if input():
            print(pol_word.upper())
            check_func(idx)

    else:
        while True:
            idx = random.randint(0, int(round(df.shape[0] * percent_of_words)))
            eng_word = df.ANG[idx]
            pol_word = df.POL[idx]
            print(eng_word, end=" - ")
            if input():
                print(pol_word.upper())
                check_func(idx)


def pol_eng(number_of_words=0):
    percent_of_words = 0.2
    if number_of_words == 1:
        idx = random.randint(0, int(round(df.shape[0] * percent_of_words)))
        eng_word = df.ANG[idx]
        pol_word = df.POL[idx]
        print(pol_word, end=" - ")
        if input():
            print(eng_word.upper())
            check_func(idx)
    else:
        while True:
            idx = random.randint(0, int(round(df.shape[0] * percent_of_words)))
            eng_word = df.ANG[idx]
            pol_word = df.POL[idx]
            print(pol_word, end=" - ")
            if input():
                print(eng_word.upper())
                check_func(idx)


def random_choice():
    while True:
        if random.randint(0, 1) == 0:
            eng_pol(1)
        else:
            pol_eng(1)


if __name__ == "__main__":
    random_choice()