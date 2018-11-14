"""Module for some basic functions, so they don't clutter run.py"""

import random


def get_roll(text):
    """Return int of the query passed in."""
    if text.startswith("d"):
        text = text.replace("d", "")

        try:
            dice = int(text)
        except ValueError:
            return 0, "Invalid input!"

        if dice < 1:
            return 0, "Rolling this dice would destroy the universe. The...*authorities* have been alerted."

        return 1, random.randint(1, dice)
    elif "d" in text:
        tokens = text.split("d")

        try:
            amount = int(tokens[0])
            dice = int(tokens[1])
        except ValueError:
            return 0, "Invalid input!"

        if dice < 1:
            return 0, "Rolling this dice would destroy the universe. The...*authorities* have been alerted."

        if amount < 1:
            return 0, "*[stares at dice forlornly]*"

        if amount > 100:
            return 0, "Don't make me roll that many dice >:("

        rolls = []
        total = 0
        for i in range(amount):
            roll = random.randint(1, dice)
            total += roll
            rolls.append(str(roll))

        return 1, "{} = {}".format(" + ".join(rolls), str(total))
    else:
        try:
            return 1, int(text)
        except ValueError:
            return 0, "Invalid input!"
