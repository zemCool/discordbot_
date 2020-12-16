import discord
import random
from discord.ext import commands
from discord.utils import get

random_greetings = [
    "How are things going?",
    "Glad to see ya!",
    "Wassup?",
    "Long time no see, huh?",
    "We missed u.",
    "How u doing?"
]

responses = [
    "Without a doubt.",
    "Yes - definitely.",
    "Signs point to yes.",
    "Cannot predict now.",
    "My reply is no.",
    "My sources say no.",
    "Very doubtful."
]

prefix = '.'

bad_language = [
    "shut up"
]

client = commands.Bot(command_prefix=prefix)


# Bot indicator
@client.event
async def on_ready():
    print('Bot is ready.')


# Greeting
@client.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f"{author}, Hello! {random.choice(random_greetings)}")


client.run('token')