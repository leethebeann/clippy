# bot.py
import os
import random
import datetime
import asyncio

import discord
from dotenv import load_dotenv
from discord.ext import commands, timers

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#variables
bot = commands.Bot(command_prefix='!')
bot.timer_manager = timers.TimerManager(bot)
pomodoro_timer = True

#to do list
todo_list = []
#three commands: !show, !add, !done
@bot.command(name='show', help="shows a user's todo list")
async def pomodoro(ctx):
    global todo_list
    #print(todo_list)
    count = 1
    
    for items in todo_list:
        listItem = "{0}. {1}".format(count, items)
        await ctx.send(listItem)
        count += 1
    


@bot.command(name='add', help="adds to a user's to do list")
async def pomodoro(ctx, *, text):
    global todo_list

    todo_list.append(text)
    #print(todo_list)
    await ctx.send("{0} has been added".format(text))

@bot.command(name='done', help="deletes a to do list item from a user's list by list item number")
async def pomodoro(ctx, *, text): #text would be the index of the todo list item
    global todo_list
    print(todo_list)

    index = int(text)
    task = todo_list[index-1]
    todo_list.pop(index-1)
    await ctx.send("Congrats for finishing a task! \"{0}\" has been removed from the list".format(task))

#pomodoro timer
@bot.command(name='pomodoro', help='Starts pomodoro timer')
async def pomodoro(ctx):

    start_message = [
        "You have 25 minutes left! Get to studying :)",
        "Only 25 more minutes to go!",
        "Get studying! 25 minutes, on the clock."
    ]

    almost_there_message = [
        "Don't give up! Only 5 more minutes ",
        "Only 5 more minutes to go. You got this ",
        "5 MORE MINUTES ",
    ]

    break_message = [
        "BREAK TIME FOR ",
        "I've got a gift: it's a 5 minute break time for  ",
        "Come back in 5 minutes ",
    ]

    while(pomodoro_timer):
        response = random.choice(start_message)
        #await ctx.send("Hey <@{0}>! You have 25 minutes left! Get to studying :)".format(ctx.author.id))
        await ctx.send("Hey <@{0}>! {1}".format(ctx.author.id, response))
        await asyncio.sleep(10)

        if(pomodoro_timer):
            response = random.choice(almost_there_message)
            await ctx.send("{1} <@{0}>!".format(ctx.author.id, response))
            await asyncio.sleep(5)

        if(pomodoro_timer):
            response = random.choice(break_message)
            await ctx.send("{1} <@{0}>!".format(ctx.author.id, response))
            await asyncio.sleep(5)

@bot.command(name='stop', help='Stops all pomodoro timers')
async def stopPomodoro(ctx):
    global pomodoro_timer 
    pomodoro_timer = False
    await ctx.send("Pomodoro stopped!")
    pomodoro_timer = True

# sets reminders
@bot.command(name='remind', help='Set a reminder for any day in the format Year/Month/Day (message)')
async def remind(ctx, time, *, text):
    #Remind to do something on a date. The date must be in ``Y/M/D`` format.
    date = datetime.datetime(*map(int, time.split("/")))
    print(date)

    bot.timer_manager.create_timer("reminder", date, args=(ctx.channel.id, ctx.author.id, text))
    
@bot.event
async def on_reminder(channel_id, author_id, text):
    channel = bot.get_channel(channel_id)

    await channel.send("Hey, <@{0}>, remember to: {1}".format(author_id, text))


''' Displays Connection of Bot to Discord Server
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.na,
        "Life is tough but so are you."me == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

'''

#motivational responses based on the keywords "tired" and "failed"
@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author == bot.user:
        return

    #add more quotes!
    fail_quote = [
        "Don't give up!",
        "Failure is only the opportunity to begin again more intelligently.",
        "You can always bounce back!",
        "Failure is an attitude, not an outcome."
    ]

    tired_quote = [
        "She's strong but she's exhausted.",
        "I know you are tired, but you have to keep going!",
        "The more you sweat in practice, the less you bleed in battle.",
        "WAKE UP!!"
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

'''

#motivational responses based on the keywords "tired" and "failed"
@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author == bot.user:
        return

    #add more quotes!
    fail_quote = [
        "Don't give up!",
        "Failure is only the opportunity to begin again more intelligently.",
        "You can always bounce back!",
        "Failure is an attitude, not an outcome."
    ]

    tired_quote = [
        "She's strong but she's exhausted.",
        "I know you are tired, but you have to keep going!",
        "The more you sweat in practice, the less you bleed in battle.",
        "WAKE UP!!"
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

'''

#motivational responses based on the keywords "tired" and "failed"
@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author == bot.user:
        return

    #add more quotes!
    fail_quote = [
        "Don't give up!",
        "Failure is only the opportunity to begin again more intelligently.",
        "You can always bounce back!",
        "Failure is an attitude, not an outcome."
    ]

    tired_quote = [
        "She's strong but she's exhausted.",
        "I know you are tired, but you have to keep going!",
        "The more you sweat in practice, the less you bleed in battle.",
        "WAKE UP!!"
    ]

    if 'failed' in message.content:
        response = random.choice(fail_quote)
        await message.channel.send(response)
    
    if 'tired' in message.content:
        response = random.choice(tired_quote)
        await message.channel.send(response)
    
        
bot.run(TOKEN)