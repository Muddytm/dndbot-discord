import config
from discord.ext import commands
import functions as f

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
            code, roll = f.get_roll(token)
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


client.run(TOKEN)
