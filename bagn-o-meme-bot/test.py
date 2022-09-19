# we import discordpy and specify intent. Intents are passed on when we create a client 
# In this intent, we will specify that we expect message with contents

from enum import Enum
import discord 
import MemePy
from MemePy.MemeLibJsonDecoder import generate_standard_meme_dict
from MemePy.MemeModel import MemeImage
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

# ------------------------------------- !bagn help embed <start> ----------------------------------------
# opening_command help|describe|templates|<template_name> [Args, either Optional or required, based on template]
# !bagn help embed, only be doing this once and reply the same embed 
# Create discord embeds 

# Keeping these global until we find a better place for these. 
# Help message embed
embed_helpmsg = discord.Embed(
    title='Bagn0Meme Bot HelpLine',
    description='Bagn0Meme bot helpline, details on how to use this shitpretzel',
    color=discord.Color.green()
)
# Wrong usage msg embed
embed_wrongusage = discord.Embed(
    title='Bitch, wrong command.',
    description='Ask fo help if ya new in town.',
    color=discord.Color.red()
)
# Available meme templates list msg embed 
embed_templateslist = discord.Embed(
    title='Meme your heart out luuuzer',
    description='List of meme templates available in this shitpretzel\'s underpants. More to come...',
    color=discord.Color.blurple() 
)

# MemeTemplates dict 
memetemplates = {}


def prep_helpmsg_embed(): 
    global embed_helpmsg  
    # Setting the baseline 
    # embed_msg.set_author(name="Bagn0Meme Bot")
    # embed_msg.set_thumbnail(url='./generated_memes/meme.png')
    embed_helpmsg.add_field(name='**Usage**', value='!bagn help|describe|templates|<template_name> [arguments (if any)]', inline=False)
    # Explain help command 
    embed_helpmsg.add_field(name='!bagn help', value='Displays these details about how to use this nutsuckler', inline=False)
    # Explain templates command
    embed_helpmsg.add_field(
        name='!bagn templates',
        value='List of all available templates at the moment. Ever growing, ever expanding.',
        inline=False
    )
    # Explain describe command 
    embed_helpmsg.add_field(
        name='!bagn describe <template_name>', 
        value='Describes the template. Some templates have required fields and some dont.\n This command describes how a template can be used',
        inline=False
    )
    # Explain the main meme command 
    embed_helpmsg.add_field(
        name='!bagn <template_name> <template_args>',
        value='This is how you meme madafaka. Select the template that you like and meme it out. Currently we support adding/replace text from certain point. Later we can add username tags, and sntching their dp and add it properly within the template',
        inline=False
    )

def prep_wrongusage_embed():
    global embed_wrongusage
    embed_wrongusage.add_field(
        name='**Lolipop for the Nicklodian gang**', 
        value='!bagn help|describe|templates|<template_name> [arguments (if any)]', 
        inline=False
    )

# Def the list of templates available, returns a dictionary with name => usage 
def prep_templateslist_embed():
    # Prepares a dict
    global memetemplates
    # Get the meme lib - returns a dict of Meme name and corresponding MemeImage obj
    memetemplates = generate_standard_meme_dict()
    # Now for each meme
    for memeobj in memetemplates:
        # Take MemeImage obj
        memeImageObj = memetemplates[memeobj]
        # Total fields, Required fields 
        total_fields = memeImageObj.text_zones
        required_fields = memeImageObj.count_non_optional()
        embed_templateslist.add_field(name=memeobj, value='Total: ' + str(len(total_fields)) + ' Req: ' + str(required_fields), inline=True)


# Then we define events, and based on those events, interaction
@client.event 
async def on_ready():
    # Prepare embeds here 
    print('Preparing Help embed msg')
    prep_helpmsg_embed()
    print('Preparing wrong usage embed')
    prep_wrongusage_embed()
    print('Preparing templates list embed')
    prep_templateslist_embed()
    # Prepare meme dictionaries here, later when dict gets updated, we can call related method to get latest data 

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
            await message.channel.send(embed=embed_wrongusage)
            return

        # now check second command and call related functions accordingly 
        if received_commands[1].lower() == 'help':
            await message.channel.send('A Cry fo help!', embed=embed_helpmsg)
        elif received_commands[1].lower() == 'describe':
            await message.channel.send('Todo - take args, check templates list')
        elif received_commands[1].lower() == 'templates':
            await message.channel.send('Things to fuck around with', embed=embed_templateslist)
        elif received_commands[1].lower() == 'testit':
            await message.channel.send('Check console debug')
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