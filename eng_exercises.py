import random
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("dictionary.csv", index_col=0)


def upload_weight(dframe, indx):
    yes_rate = 1.3
    no_rate = 0.7
    if (input("Correct ? [Y/N] ").upper()) == "Y":
        dframe.weights[indx] *= yes_rate
    else:
        dframe.weights[indx] *= no_rate
    print()


def eng_pol(number_of_words=0):
    if number_of_words == 1:
        idx = random.randint(0, df.shape[0])
        eng_word = df.ANG[idx]
        pol_word = df.POL[idx]
        print(eng_word, end=" - ")
        if input():
            print(pol_word.upper())
            upload_weight(df, idx)

    else:
        while True:
            idx = random.randint(0, df.shape[0])
            eng_word = df.ANG[idx]
            pol_word = df.POL[idx]
            print(eng_word, end=" - ")
            if input():
                print(pol_word.upper())
                upload_weight(df, idx)


def pol_eng(number_of_words=0):
    if number_of_words == 1:
        idx = random.randint(0, df.shape[0])
        eng_word = df.ANG[idx]
        pol_word = df.POL[idx]
        print(pol_word, end=" - ")
        if input():
            print(eng_word.upper())
            upload_weight(df, idx)
    else:
        while True:
            idx = random.randint(0, df.shape[0])
            eng_word = df.ANG[idx]
            pol_word = df.POL[idx]
            print(pol_word, end=" - ")
            if input():
                print(eng_word.upper())
                upload_weight(df, idx)


def random_choice():
    while True:
        if random.randint(0, 1) == 0:
            eng_pol(1)
        else:
            pol_eng(1)


if __name__ == "__main__":
    random_choice()