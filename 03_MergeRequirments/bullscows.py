import random
import urllib.request
import os
import argparse
import sys

def bullscows(guess: str, secret: str) -> (int, int):
    bulls = [(guess[i] == secret[i]) for i in range(min(len(guess),len(secret)))].count(True)
    cows = len(set(guess).intersection(set(secret)))
    return (bulls, cows)

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = random.choice(words)
    ask_num = 0
    bulls = 0
    while bulls != len(secret):
        bulls, cows = bullscows(ask("Введите слово: ", words), secret)
        inform("Быки: {}, Коровы: {}", bulls, cows)
        ask_num += 1
    return ask_num

def ask(prompt: str, valid: list[str]=None) -> str:
    guess = input(prompt)
    if valid is not None:
        while guess not in valid:
            guess = input(prompt)
    return guess

def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print("usage: python -m bullscows <dict_path> <word_len>")
        sys.exit(0)

    if len(sys.argv) == 3:
        word_len = int(sys.argv[2])

    dict_path = sys.argv[1]

    try:
        with urllib.request.urlopen(dict_path) as f:
            word_list = f.read().decode().split()
    except Exception:
        with open(dict_path) as f:
            word_list = f.read().split()

    print("Total attempts:", gameplay(ask, inform, word_list))