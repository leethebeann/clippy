# bot.py
import os
import random
import datetime
import asyncio
import wolframalpha 
import youtube_dl

import discord
from dotenv import load_dotenv
from discord.ext import commands, timers
from googlesearch import search


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#variables
bot = commands.Bot(command_prefix='!')
bot.timer_manager = timers.TimerManager(bot)
pomodoro_timer = True
showTimer = False
breakTime = False
todo_list = [] #to do list


# To Do List -- three commands: !show, !add, !done
@bot.command(name='show', help="shows a user's todo list")
async def toDoList(ctx):
    global todo_list
    #print(todo_list)
    count = 1

    if len(todo_list) == 0:
        await ctx.send("Congrats! Your To Do List is empty!")
    
    for items in todo_list:
        listItem = "{0}. {1}".format(count, items)
        await ctx.send(listItem)
        count += 1

    
@bot.command(name='add', help="adds to a user's to do list")
async def addToList(ctx, *, text):
    global todo_list

    todo_list.append(text)
    #print(todo_list)
    await ctx.send("{0} has been added".format(text))

@bot.command(name='done', help="deletes a to do list item from a user's list by list item number")
async def removeFromList(ctx, *, text): #text would be the index of the todo list item
    global todo_list
    print(todo_list)

    index = int(text)
    task = todo_list[index-1]
    todo_list.pop(index-1)
    await ctx.send("Congrats for finishing a task! \"{0}\" has been removed from the list".format(task))

# Pomodoro study timer -- commands: !pomodoro, !stop, !break, !time
@bot.command(name='pomodoro', help='starts pomodoro timer')
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
    
    #global variables 
    global pomodoro_timer
    pomodoro_timer = True
    global breakTime
    breakTime = False
    global showTimer 
    showTimer = False

    t = 16 #pomodoro time in seconds

    while(t):
        mins, secs = divmod(t, 60) 
        timer = "{:02d}:{:02d}".format(mins, secs) 
        await asyncio.sleep(1) 
        t -= 1
        
        #displays time remaining
        if(showTimer):
            await ctx.send(timer) 
            showTimer = False

        #stops clock
        if(pomodoro_timer == False):
            break
 
        #start of clock
        elif(pomodoro_timer == True and t == 15):
            response = random.choice(start_message)
            await ctx.send("Hey <@{0}>! {1}".format(ctx.author.id, response))

        #5 minute left alert
        elif(pomodoro_timer == True and t == 6 and breakTime == False):
            response = random.choice(almost_there_message)
            breakTime = True
            await ctx.send("{1} <@{0}>!".format(ctx.author.id, response))

        #break time
        elif(pomodoro_timer == True and t == 0):
            if(breakTime == True):
                response = random.choice(break_message)
                await ctx.send("{1} <@{0}>!".format(ctx.author.id, response))
                t = 5
                breakTime = False
            else:
                t = 15
                #breakTime == True
        

@bot.command(name='stop', help='stops all pomodoro timers')
async def stopPomodoro(ctx):
    global pomodoro_timer 
    pomodoro_timer = False
    await ctx.send("Pomodoro stopped!")

@bot.command(name='break', help='stops all pomodoro timers')
async def startBreak(ctx):
    global breakTime 
    breakTime = False
    await ctx.send("Starting Break Time now!")

@bot.command(name='time', help='Displays time remaining for pomodoro clock') 
async def timeRemaining(ctx):
    global showTimer
    showTimer = True
    await ctx.send("Here is the time remaining on the Pomodoro Clock:")

# Sets reminders -- !remind
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

# Motivational responses based on the keywords "tired" and "failed"
@bot.event
async def on_message(message):
    await bot.process_commands(message)

    # Animal emoji reactions!
    reactions = ['🐮', '🐷', '🐒', '🐼', '🐥', '🦕', '🐙']
    #for emoji in reactions: 
    emoji = random.choice(reactions)
    await message.add_reaction(emoji)

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

    die_quote = [
        "You can do this!",
        "Your pet would want you alive",
        "Let's eat ice cream instead",
        "You're too hot to die >.<"
    ]

    if 'failed' in message.content:
        response = random.choice(fail_quote)
        await message.channel.send(response)
    
    if 'tired' in message.content:
        response = random.choice(tired_quote)
        await message.channel.send(response)
    
    if 'die' in message.content:
        response = random.choice(die_quote)
        await message.channel.send(response)

#Google Search Feature
#Takes in command (!search) and the search terms
@bot.command(name='search', help='google search a topic of interest (Enter the topic you want to search)')
async def googleSearch(ctx, *, text):
    query = text
    for result in search(query, tld="co.in", num=3, stop=3, pause=2):
        await ctx.send(result)

#Wolfram Alpha Feature
#Takes in command (!wolf) and the math problem/equation
@bot.command(name='wolf', help='use wolfram alpha to search put math problems and etc')
async def wolfram(ctx, *, text):
    APP_ID = os.getenv('APP_ID')
    client = wolframalpha.Client(APP_ID) 
    
    res = client.query(text) 
    answer = next(res.results).text 
    await ctx.send("The answer is: {0}".format(answer))


# Play hangman with the study bot 
@bot.command(name='hangman', help='play hangman with the study bot')
async def hangman(ctx):
    thisdict = {
        "Movies" : ["Hunger Games", "Good Will Hunting", "The Way Way Back", "Avengers End Game", "Inception"],
        "Netflix Shows" : ["Peaky Blinders", "Narcos", "New Girl", "Criminal Minds", "Greys Anatomy", "Avatar The Last Airbender"],
        "Celebrities" : ["Brad Pitt", "Kanye West", "Miley Cyrus", "Jennifer Aniston", "Beyonce", "Jennifer Lopez", "Will Smith", "Justin Bieber"],
        "Animals" : ["Monkey", "Cow", "Sloth", "Shark", "Kangaroo", "Zebra", "Giraffe", "Penguins", "Python"],
        "Vegetables" : ["Broccoli", "Spinach", "Kale", "Eggplant", "Cucumber",  "Artichoke", "Cauliflower", "Zucchini"]
    }
    topic_list = ["Movies", "Netflix Shows", "Celebrities", "Animals", "Vegetables"] 

    topic = random.choice(topic_list)
    await ctx.send("Let's play Hangman! The topic is {}.".format(topic))
    word_list = thisdict.get(topic)
    word_chosen = random.choice(word_list)

    lives_remaining  =  9
    guesses = ''
    while (lives_remaining > 0):
        incorrect = 0
        for char in word_chosen:
            if char in guesses:
                await ctx.send(char)
            else:
                await ctx.send('_')
                incorrect += 1
        
        if incorrect == 0:
            await ctx.send("You won! :)")
            break
        
        guess = ''
        if len(guess) < 1:
            guess = input("Guess a letter") 
        
        guesses += guess

        if guess not in word_chosen:
            lives_remaining -= 1
            await ctx.send("Incorrect letter")

        await ctx.send("You have {} lives remaining".format(lives_remaining))

        if lives_remaining == 0:
            await ctx.send("Man is dead :(")     
    
    await ctx.send("The word was: {}".format(word_chosen))



#yt
@bot.command(name='yt', help='plays youtube video')
async def yt(ctx, url):
    author = ctx.message.author
    voice_channel = author.voice_channel
    vc = await client.join_voice_channel(voice_channel)

    player = await vc.create_ytdl_player(url)
    player.start()

bot.run(TOKEN)