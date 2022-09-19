# we import discordpy and specify intent. Intents are passed on when we create a client 
# In this intent, we will specify that we expect message with contents

from enum import Enum
import discord 
import MemePy
import os
import time
from dotenv import load_dotenv
load_dotenv()

# Using intents, we need to be able to read message_contents
intents = discord.Intents.default()
intents.message_content = True 

# Activity to indicate shitshow 
# It either works as activity param set 
# client = discord.Client(intents=intents, activity=discord.Game(name='The Meme Game'))
# Or
# Setting activity manually 
activity = discord.Activity(name='YOU, bitch 0.o', type=discord.ActivityType.watching)
client = discord.Client(intents=intents, activity=activity)

# Predefined commands 
opening_command = '!bagn'

# opening_command help|describe|templates|<template_name> [Args, either Optional or required, based on template]
# !bagn help embed, only be doing this once and reply the same embed 
# Create discord embed for help details 
embed_msg = discord.Embed(
    title='Bagn0Meme Bot HelpLine',
    description='Bagn0Meme bot helpline, details on how to use this shitpretzel',
    color=discord.Color.green()
)
    
# Setting the baseline 
embed_msg.set_author(name="Bagn0Meme Bot")
#embed_msg.set_thumbnail(url='./generated_memes/meme.png')
embed_msg.add_field(name='**Usage**', value='!bagn help|describe|templates|<template_name> [arguments (if any)]', inline=False)
# Explain help command 
embed_msg.add_field(name='!bagn help', value='Displays these details about how to use this nutsuckler', inline=False)
# Explain templates command
embed_msg.add_field(
    name='!bagn templates',
    value='List of all available templates at the moment. Ever growing, ever expanding.',
    inline=False
)
# Explain describe command 
embed_msg.add_field(
    name='!bagn describe <template_name>', 
    value='Describes the template. Some templates have required fields and some dont.\n This command describes how a template can be used',
    inline=False
)
# Explain the main meme command 
embed_msg.add_field(
    name='!bagn <template_name> <template_args>',
    value='This is how you meme madafaka. Select the template that you like and meme it out. Currently we support adding/replace text from certain point. Later we can add username tags, and sntching their dp and add it properly within the template',
    inline=False
)

# Then we define events, and based on those events, interaction
@client.event 
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event 
async def on_message(message):
    if message.author == client.user:
        return 

    # If the message content starts with opening_command, enter this and split the received args
    if message.content.startswith(opening_command):
        # Check which command we received 
        received_commands = message.content.split()

        # opening_command help|describe|templates|<template_name> [Args, either Optional or required, based on template]
        # received commands length has to be 2 or more. Ex: !bagn help 
        if len(received_commands) < 2:
            await message.channel.send('Todo - simple usage embed')
            return

        # now check second command and call related functions accordingly 
        if received_commands[1].lower() == 'help':
            await message.channel.send('A Cry fo help!', embed=embed_msg)
        elif received_commands[1].lower() == 'describe':
            await message.channel.send('Todo - take args, check templates list')
        elif received_commands[1].lower() == 'templates':
            await message.channel.send('Todo - return templates list - fidn a better way to present images')
        else:
            # take meme template name
            meme_template_name = received_commands[1].lower()
            # Check if it's present within currently available templates 
            # << Check Check >>
            # Check required args Optional + Required 
            # << Check Check 2 >>
            # Generate using MemePy.save_meme_to_disk 

            # Refund.... I mean, return 
            await message.channel.send('---- Currently Under Construction --- ')

        # # It has to start with !bagn or any other predefined command 
        # # Clear path - if meme.png exists, delete it 
        # if(os.path.exists('./generated_memes/meme.png')):
        #     os.remove('./generated_memes/meme.png')
        
        # # MemePy expects args, let's provide following and see what happens
        # # template = 'MeAlsoMe'     - Things are case sensetive here 
        # # path = ./generated_memes dir 
        # # args = depending upon the meme template 

        # # Options = None at this time
        # memeObj = MemePy.save_meme_to_disk(
        #     'MeAlsoMe',
        #     './generated_memes', [
        #         'Flip burgers',
        #         'into Bagners'
        #     ]
        # )

        # # As MemePy creates meme.png file, we need to rename it to something 
        # # we take that filename that's eventually be passed into discord.File() 
        # # Later we can use this to delete the temp file that we created - Depends, do we wanna keep them?
        # memefilename = './generated_memes/meme.png'

        # # Now it requires two more things, depending upon which meme template is selected 
        # # you need text args 
        # #- ----- Scratch that and now get file object from discord 
        # # need an fp?
        # fp = open(memefilename, 'rb')
        # discfile = discord.File(fp=fp, filename=memefilename, spoiler=False, description='Return of the meme')
        # fp.close()
        # # Returning result would be an image 
        # await message.channel.send('Here ya go cowboy', file=discfile)

    if 'bitch' in message.content:
        await message.channel.send('Wooaahh there cowboy. Eeassyy there!')

client.run(os.getenv("DISCORD_TOKEN_DEV_SERVER"))