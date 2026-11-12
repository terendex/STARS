#!/usr/bin/env python3
"""Giausar guards a flag behind a password.

Run it with:  python3 giausar.py
"""

# The flag, locked with the password. Only the right password unlocks it.
LOCKED_FLAG = bytes.fromhex("@LOCKED@")


def unlock(password):
    key = password.encode()
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(LOCKED_FLAG)).decode()


guess = input("Password: ").strip()

if guess == "@PASSWORD@":
    print("Giausar opens its vault. " + unlock(guess))
else:
    print("Wrong password.")
