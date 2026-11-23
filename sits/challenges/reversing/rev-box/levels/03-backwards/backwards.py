#!/usr/bin/env python3
"""The bakery's recipe vault. Only the right password opens it.

Run it with:  python3 backwards.py
"""

SECRET = "@SECRET@"

# The flag, locked with the password. Only the right password unlocks it.
LOCKED_FLAG = bytes.fromhex("@LOCKED@")


def unlock(password):
    key = password.encode()
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(LOCKED_FLAG)).decode()


guess = input("Password: ").strip()

if guess == SECRET[::-1]:
    print("The vault opens. " + unlock(guess))
else:
    print("Wrong password.")
