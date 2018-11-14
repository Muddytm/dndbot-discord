import config
from discord.ext import commands
import random

TOKEN = config.app_token
BOT_PREFIX = "!"
client = commands.Bot(command_prefix=commands.when_mentioned_or(BOT_PREFIX))

@client.event
async def on_ready():
    print ("Logged in as")
    print (client.user.name)
    print (client.user.id)
    print ("------")


@client.command(pass_context=True)
async def test(ctx, stuff=""):
    """Test for basic command input."""
    await client.say("*[ominous robot noises]*")


@client.command(pass_context=True)
async def roll(ctx, *stuff):
    """TIME TO ROLL THE DICE"""
    if not stuff:
        await client.say("*[rolls around on the ground]*")
        await client.say("(You might want to specify what you're rolling - examples: `!roll d20`, `!roll 2d6`, `!roll 1000d2`)")
        return
    else:
        stuff = "".join(stuff)
        stuff = stuff.split("+")

        total = 0
        rolls = []
        for token in stuff:
            code, roll = get_roll(token)
            roll = str(roll)

            if code == 0:
                await client.say(roll)
                return

            #print (roll)
            total += int(roll.split()[-1])
            rolls.append(roll)

        if len(rolls) > 1:
            await client.say("{} rolled **{}**! ({})".format(ctx.message.author.mention, str(total), ", ".join(rolls)))
        else:
            if len(rolls[0].split()) > 1:
                thing = rolls[0].split("=")[0]
                thing = "".join(thing).replace(" ", "").split("+")
                await client.say("{} rolled **{}**! ({})".format(ctx.message.author.mention, str(total), ", ".join(thing)))
            else:
                await client.say("{} rolled **{}**!".format(ctx.message.author.mention, str(total)))


@client.command(pass_context=True)
@commands.has_any_role("GM", "Caleb")
async def scram(ctx, stuff=""):
    """Get outta here, bot!"""
    await client.say("I'm outta here, gramps! *[skates away on heelies]*")
    await client.logout()


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


client.run(TOKEN)
