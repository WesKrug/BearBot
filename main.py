# Work with Python 3.6
import os
import discord
from dotenv import load_dotenv
import dice

load_dotenv()
client = discord.Client()

@client.event
async def on_message(message):
    if (message.content.startswith('/')):
        ooc_message = message.content[1:]
        if (message.mentions):
            for pinged in message.mentions:
                ooc_message = ooc_message.replace("<@!"+str(pinged.id)+">", "@"+pinged.nick)
                print(ooc_message)
        await message.delete()
        await message.channel.send('```fix\n{0}: {1}```'.format(message.author.display_name, ooc_message))
    
    
    if (message.content.startswith("!roll") or message.content.startswith("!Roll")):
        rollString = ""
        plus = message.content.find('+') #Equals -1 if dne
        minus = message.content.find('-') #Equals -1 if dne

        try:
            if (plus != -1):
                rollString = message.content[6:message.content.find('+')]
            elif (minus != -1):
                rollString = message.content[6:message.content.find('-')]
            else:
                rollString = message.content[6:]

            result = dice.roll(rollString)
        except:
            await message.channel.send("```fix\n-Bad roll: '{0}'. Do better.```".format(message.content))
            return
        total = 0
        for i in result:
            total += i
        try:
            if (plus != -1):
                total += int(message.content[plus+1:])
            if (minus != -1):
                total -= int(message.content[minus+1:])
        except:
            await message.channel.send("```diff\n-Couldn't parse modifier: '{0}'. Do better.```".format(message.content[6:]))

        resultMessage = "```glsl\n{2} rolled [{3}]: {0}\nTotal with modifiers: {1}```".format(result, total, message.author.display_name, message.content[6:])
        
        await message.channel.send(resultMessage)
        try:
            await message.delete()
        except:
            return

@client.event
async def on_ready():
    return

client.run(os.getenv('DISCORD_TOKEN'))