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
        text = stuff[0].lower()

        if text.startswith("d"):
            text = text.replace("d", "")

            try:
                mod = 0
                if "+" in text:
                    mod = int(text.split("+")[1])
                    text = text.split("+")[0]

                dice = int(text)
            except ValueError:
                await client.say("Invalid input!")
                return

            if dice < 1:
                await client.say("Rolling this dice would destroy the universe. The...*authorities* have been alerted.")
                return

            roll = random.randint(1, dice)
            if mod == 0:
                await client.say("{} rolled a **{}**!".format(ctx.message.author.mention, str(roll)))
            else:
                await client.say("{} rolled a **{}** (+ {}) -> **{}**!".format(ctx.message.author.mention, str(roll), str(mod), str(roll + mod)))
        elif "d" in text:
            tokens = text.split("d")

            try:
                amount = int(tokens[0])
                dice = int(tokens[1])
            except ValueError:
                await client.say("Invalid input!")
                return

            if dice < 1:
                await client.say("Rolling this dice would destroy the universe. The...*authorities* have been alerted.")
                return

            if amount < 1:
                await client.say("*[stares at dice forlornly]*")
                return

            if amount > 100:
                await client.say("Don't make me roll that many dice >:(")
                return

            rolls = []
            total = 0
            for i in range(amount):
                roll = random.randint(1, dice)
                total += roll
                rolls.append(str(roll))

            await client.say("{} rolled a total of **{}**! ({})".format(ctx.message.author.mention, str(total), " + ".join(rolls)))


@client.command(pass_context=True)
@commands.has_any_role("GM", "Caleb")
async def scram(ctx, stuff=""):
    """Get outta here, bot!"""
    await client.say("I'm outta here, gramps! *[skates away on heelies]*")
    await client.logout()

client.run(TOKEN)
