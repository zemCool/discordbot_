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


# Chat filter
@client.event
async def on_message(message):
    await client.process_commands(message)
    msg = message.content.lower()
    if msg in bad_language:
        await message.delete()


# Disconnect from a voice channel
@client.command(name='disconnect_', help='bot disconnects from the voice channel.', aliases=['disconnect'])
async def disconnect_(ctx):
    await ctx.channel.purge(limit=1)
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f'Bot is disconnected from: {channel}')
    else:
        voice = await channel.connect


# Join to a voice channel
@client.command(name='join', help='bot joins to voice channel.')
async def join(ctx):
    await ctx.channel.purge(limit=1)
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Bot joined to: {channel}')


# An 8ball game
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

# Messages clearer

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)


# An error with clearer
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete.')


# Kick
@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member}")


# Ban
@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} is banned.')


# Unban
@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    await ctx.channel.purge(limit=1)
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        await ctx.guild.unban(user)
        await ctx.send(f'{user.mention} is unbanned.')
        return


# Unknown command
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')


client.run('token')
