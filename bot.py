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


bot = commands.Bot(command_prefix='!')
bot.timer_manager = timers.TimerManager(bot)

pomodoro_timer = True

@bot.command(name='stop', help='Stops pomodoro timer')
async def stopPomodoro(ctx):
    global pomodoro_timer 
    pomodoro_timer = False
    print(pomodoro_timer)
    await ctx.send("Pomodoro stopped!")

#pomodoro timer
@bot.command(name='pomodoro', help='Starts pomodoro timer')
async def pomodoro(ctx):
    while(pomodoro_timer):
        print(pomodoro_timer)
        await ctx.send("You have 25 minutes left! Get to studying :)")
        
        await asyncio.sleep(10)

        await ctx.send("Start your break!")
        
        await asyncio.sleep(5)




# sets reminders
@bot.command(name='remind', help='Reminder')
async def remind(ctx, time, *, text):
    """Remind to do something on a date.

    The date must be in ``Y/M/D`` format."""
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
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

'''

#event responses
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