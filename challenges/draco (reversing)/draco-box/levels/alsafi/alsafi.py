#!/usr/bin/env python3
"""Alsafi guards a flag. It never writes its password down: it checks your
guess one letter at a time instead.

Run it with:  python3 alsafi.py
"""

# The flag, locked with the password. Only the right password unlocks it.
LOCKED_FLAG = bytes.fromhex("@LOCKED@")


def unlock(password):
    key = password.encode()
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(LOCKED_FLAG)).decode()


def check(guess):
    """Checks the guess one letter at a time, in no particular order."""
    if len(guess) != @LENGTH@:
        return False
@CHECKS@
    return True


guess = input("Password: ").strip()

if check(guess):
    print("Alsafi lets you in. " + unlock(guess))
else:
    print("Wrong password.")
