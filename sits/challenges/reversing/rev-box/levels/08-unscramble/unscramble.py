#!/usr/bin/env python3
"""The ice cream shop's secret menu. It scrambles the password you type, then
compares the result with the scrambled copy of the real password that it keeps.

Run it with:  python3 unscramble.py
"""
import base64

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

# The real password, already scrambled.
SCRAMBLED = "@SCRAMBLED@"

# The flag, locked with the password. Only the right password unlocks it.
LOCKED_FLAG = bytes.fromhex("@LOCKED@")


def shift(word, places):
    """Moves every letter the given number of places along the alphabet, so a
    shift of 1 turns a into b, and z wraps round to a."""
    return "".join(ALPHABET[(ALPHABET.index(letter) + places) % 26] for letter in word)


def scramble(word):
    word = word[::-1]
    word = shift(word, 3)
    word = base64.b64encode(word.encode()).decode()
    return word


def unlock(password):
    key = password.encode()
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(LOCKED_FLAG)).decode()


guess = input("Password: ").strip().lower()

if not guess or any(letter not in ALPHABET for letter in guess):
    print("The password is only letters.")
elif scramble(guess) == SCRAMBLED:
    print("Secret menu unlocked. " + unlock(guess))
else:
    print("Wrong password.")
