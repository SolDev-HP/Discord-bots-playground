# we import discordpy and specify intent. Intents are passed on when we create a client 
# In this intent, we will specify that we expect message with contents

from cgitb import grey
from enum import Enum
from random import seed
from random import randint 
import discord 
import MemePy
from MemePy.MemeLibJsonDecoder import generate_standard_meme_dict
from MemePy.MemeModel import MemeImage
import os
import time
from dotenv import load_dotenv
from pathlib import Path
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
# MemeTemplates dict 
memetemplates = {}
# Whackiness comes from here 
whackyreplies = [
    'I wanna be a cowboy, so I can run away from here',
    'Get ready to be disappointed like your parents',
    '[Landlord] Where\'s mah money at chigga, [Louz] I don\'t kno...',
    'It\'s always delightful when someone calls me. Except you bitch, you a cockroach',
    'Do ya brain even braincell bro?!',
    'Tell me to chill and calling me kiddo! Fck You',
    'I don\'t think you\'re acting stupid. I think it\'s totally a real thing',
    'Bilbo gave me an eDick so I can fck ya up!',
    'Zigzaggin through life ya luuuzer. Hop on the ride',
    'Do you even life bro? You should try it, I heard it\'s what you\'re suppose to do',
    'You dare waste my time in this?',
    'Beep-Boop! I\'m a bot and no I don\'t grant wishes'
]

# Whacky examples for describe to function sanely 
describe_examples = {
    'mealsome' : [
        'Testing this one function and go to sleep',
        'Sleep is fo da weak'
    ],
    'itsretarded' : ['KOV is the greatest!'],
    'headache' : ['Livin next to Ruzziya'],
    'itstime' : ['Bringin back old school things!!', 'Dis fucker has no idea what he\'s doing'],
    'classnote' : ['You a luuzer if ya don have a bagner'],
    'nutbutton' : ['BUY BAGNER'],
    'pills' : ['Buying Bagners'],
    'balloon' : [
        'Me',
        'Freedom and wisdom of life',
        'Me'
    ],
    'classy' : [
        'Cum',
        'Creme de la Penis'
    ],
    'cola' : ['Life', 'Bagners'],
    'loud' : ['My Sweep Annoucements'],
    'milk' : ['Using KOV\'s name in meme'],
    'finally' : ['Touched boob instead of grass'], 
    'cliff' : ['KOV stopped drinking', 'Hah! as if!']
    # more to join soon
}

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
# Describe a template msg embed 
embed_describetemplate = discord.Embed(
    title='Meme Template Description',
    description='Spillin some wisdom from mah cup, don\'t get caught sleepin bitchh!!',
    color=discord.Color.blue()
)


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

def prep_wrongusage_embed(which_command):
    global embed_wrongusage
    embed_wrongusage.clear_fields()
    if which_command == 'general':
        embed_wrongusage.add_field(
            name='**Lolipop for the Nicklodian gang**', 
            value='!bagn help|describe|templates|<template_name> [arguments (if any)]', 
            inline=False
        )
    else:
        embed_wrongusage.add_field(
            name='**Lolipop for the Nicklodian gang**', 
            value='!bagn describe <template_name>', 
            inline=False
        )

# Def the list of templates available, returns a dictionary with name => elements (required + optional) 
def prep_templateslist_embed():
    # Prepares a dict
    global memetemplates
    memetemplates.clear()
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

# function to get the given template. Take the arg from 
# Expect this to return the embed that we want to use
def prep_describe_template_embed(template_name):
    global embed_describetemplate
    embed_describetemplate.clear_fields()
    # Reprep Title 
    embed_describetemplate.title = '[ ' + str(template_name).lower() + ' ] - Meme Template usage details'
    # Check if we have this template 
    for template in memetemplates:
        if template_name == str(template).lower():
            embed_describetemplate.add_field(
                name='**Template Name**',
                value=template,
                inline=False
            ) 
            # Take the memeImage list
            memeImageObj = memetemplates[template]
            # Total fields, Required fields 
            total_fields = memeImageObj.text_zones
            required_fields = memeImageObj.count_non_optional()
            embed_describetemplate.add_field(
                name='**Fields**',
                value='Total Fields: ' + str(len(total_fields)) + ' | Required Fields: ' + str(required_fields),
                inline=False
            )

            # Here we need to add image that is generated by the example that we give
            value_prep = '!bagn ' + template_name
            for field in range(0, len(total_fields)):
                value_prep += ' "' + describe_examples[template_name][field] + '"'
                if field < len(total_fields) - 1:
                    value_prep += ' +'

            embed_describetemplate.add_field(
                name='**Usage Example**',
                value=value_prep,
                inline=False
            )
            
            # Now the hard part, getting the image and generate the meme for given example 
            describe_meme = MemePy.save_meme_to_disk(
                template,
                './describe_examples', 
                describe_examples[template_name]
            )
            
            # customfilename ?
            custfilename = template_name + str(time.time()).split()[0] + '.png'
            if Path('./describe_examples/meme.png').exists():
                os.rename('./describe_examples/meme.png', './describe_examples/' + custfilename)
            elif Path('./describe_examples/meme.jpg').exists():
                os.rename('./describe_examples/meme.jpg', './describe_examples/' + custfilename)
            else:
                print('What da fuck, why are you here')
            meme_file = discord.File('./describe_examples/'+custfilename, filename=custfilename)
            embed_describetemplate.set_image(url='attachment://'+custfilename)

            return embed_describetemplate, meme_file # do something here as we found it - potentially return 

    # If we reach here, it means we didn't find the template 
    # Prepare error spittin embed 
    embed_templateNotFound = discord.Embed(
        title='You sure bruv?',
        description='All these meme in the library and you came up with a name that just doesn\'t vibe with em. Try harded madafaka',
        color=discord.Color.red()
    )
    ## Add related fields and return this embed to be sent back
    return embed_templateNotFound, ''

# Then we define events, and based on those events, interaction
@client.event 
async def on_ready():
    # Prepare embeds here 
    print('Preparing Help embed msg')
    prep_helpmsg_embed()
    print('Preparing templates list embed')
    prep_templateslist_embed()
    # Prepare meme dictionaries here, later when dict gets updated, we can call related method to get latest data 
    # Prepare randomness seed 
    seed(time.time())
    print(f'We have logged in as {client.user}')

@client.event 
async def on_message(message):
    if message.author == client.user:
        return 

    # If the message content starts with opening_command, enter this and split the received args
    if message.content.startswith(opening_command):
        # Check which command we received 
        received_commands = message.content.split()

        # Give me randomnessss 
        pickup_line = randint(0, len(whackyreplies) - 1)
        # opening_command help|describe|templates|<template_name> [Args, either Optional or required, based on template]
        # received commands length has to be 2 or more. Ex: !bagn help 
        if len(received_commands) < 2:
            prep_wrongusage_embed('general')
            await message.channel.send(whackyreplies[pickup_line], embed=embed_wrongusage)
            return

        # now check second command and call related functions accordingly 
        if received_commands[1].lower() == 'help':
            await message.channel.send(whackyreplies[pickup_line], embed=embed_helpmsg)
        elif received_commands[1].lower() == 'describe':
            # Do we have template_name as arg?
            if(len(received_commands) <= 2):
                # We don't have template name - have it known!
                prep_wrongusage_embed('describe')
                await message.channel.send('Describe what? My jingdingler?', embed=embed_wrongusage)
            else:
                # So we have a template name now, send this name to preparator
                # we wont return any file when errors occur, so till we find a better way, conditional returns 
                # @Todo : find a better way to do this
                (returned_embed, example_file_meme) = prep_describe_template_embed(received_commands[2])
                if example_file_meme:
                    await message.channel.send(whackyreplies[pickup_line], file=example_file_meme, embed=returned_embed)
                else:
                    await message.channel.send(whackyreplies[pickup_line], embed=returned_embed)

        elif received_commands[1].lower() == 'templates':
            await message.channel.send(whackyreplies[pickup_line], embed=embed_templateslist)
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