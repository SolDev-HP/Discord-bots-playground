# we import discordpy and specify intent. Intents are passed on when we create a client 
# In this intent, we will specify that we expect message with contents

from enum import Enum
import discord 
import MemePy
import os
import time
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)

# Predefined commands 
opening_command = '!bagn'

# opening_command help|describe|templates|<template_name> [Args, either Optional or required, based on template]


def help_function():
    return 'Help function called'

def templates_function():
    return 'Templates List function called'

def meme_template_function():
    return 'Trying to meme here '

def describe_template():
    return 'Template description summoned'

def wrong_command_try_again():
    return 'Wrong command bitch, try again'


class ChooseAction(Enum):
    # Help command, describe how !bagn command works 
    helpfunction = (help_function,)
    # Describe template command, gives details about given template name
    describefunction = (describe_template,)
    # Lists available meme templates - this would need pagination later @Todo: think about reply's length
    templatesfunction = (templates_function,)
    # Main meme command
    memefunction = (meme_template_function,)
    # Just incase we enter wrong commands 
    wrongnessfunction = (wrong_command_try_again,)

    # Now based on class's enum selection, we'll be able to call corresponding function
    # that's cool 
    def __call__(self, *args, **kwargs):
        return self.value[0](*args, **kwargs)

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
            await message.channel.send(ChooseAction.wrongnessfunction())
            return

        # now check second command and call related functions accordingly 
        if received_commands[1].lower() == 'help':
            await message.channel.send(ChooseAction.helpfunction())
        elif received_commands[1].lower() == 'describe':
            await message.channel.send(ChooseAction.describefunction())
        elif received_commands[1].lower() == 'templates':
            await message.channel.send(ChooseAction.templatesfunction())
        else:
            # Whatever this is, should be considered potential meme-template name 
            await message.channel.send(ChooseAction.memefunction())

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

    # So MemePy works with these arguments
    # MemePy <path> <template> <*args> <*options>

    # path - where you'll be storing generated memes 
    # template - predefined templates present in MemePy library - Details in MemePy/Resources/MemeLibrary/builtin.JSON
    # args - all the arguments that are placed onto the template 
    # options - Options are passed with {} - supported option is stretch 




client.run(os.getenv("DISCORD_TOKEN_DEV_SERVER"))