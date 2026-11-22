#!/usr/bin/env python3
"""Rastaban, in the dragon's head, guards a flag.

Run it with:  python3 rastaban.py
"""

SECRET = "@SECRET@"

# The flag, locked with the password. Only the right password unlocks it.
LOCKED_FLAG = bytes.fromhex("@LOCKED@")


def unlock(password):
    key = password.encode()
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(LOCKED_FLAG)).decode()


guess = input("Password: ").strip()

if guess == SECRET[::-1]:
    print("Rastaban nods. " + unlock(guess))
else:
    print("Wrong password.")
