import discord
from discord.ext import tasks
import random
import requests
import time
from termcolor import colored, cprint
import re
import string
import os 

import config
from data import pokemon

poketwo_ID =716390085896962058
#####################

class MyClient (discord.Client):
    def __init__(self, allowed_channels):
        super().__init__()
        self.allowed_channels = allowed_channels

    async def on_ready(self):
        print("~The Program is ready!~")
        self.spam_channels = await self.get_channels()
        self.spammer.start()
        self.data = pokemon.DataManager()
    
    async def get_channels(self):
        channels = []
        for channel_ID in config.SPAM_CHANNELS:
            channels.append(self.get_channel(channel_ID))
        return channels

    @tasks.loop(seconds=3)
    async def spammer (self):
        channel = random.choice(self.spam_channels)
        try:
            await channel.send(' '.join(random.sample(string.ascii_letters+string.digits,50)*20))
        except:
            pass

    async def on_message (self, message):

        if "$say " in message.content and message.channel.id in self.allowed_channels:
          msg = message.content.strip("$say ")
          await message.channel.send(msg)

        if message.author.id == poketwo_ID and message.channel.id in self.allowed_channels:
            for embed in message.embeds:
                if ("pokémon" in embed.title):
                    print("a poke appeared")
                    time.sleep(2)
                    await message.channel.send("p!hint")

                    def check_message(m):
                        return (m.author.id == poketwo_ID and m.channel.id == message.channel.id and "the pokémon is" in m.content.lower()) 
                    
                    def check_caught(m):
                        return (m.author.id == poketwo_ID and m.channel.id in self.allowed_channels) 
                    
                    try:
                        hint_message = await self.wait_for('message', timeout=9, check=lambda m: check_message(m))
                    except:
                        await message.channel.send("p!hint")
                        try:
                            hint_message = await self.wait_for('message', timeout=5, check=lambda m: check_message(m))
                        except:
                            cprint("COOLDOWN: MISSED POKE", "magenta")
                            return
                    
                    content = hint_message.content.replace("\\","").lower()
                    
                    try:
                        hint = re.search('the pokémon is (.+?)\.', content).group(1)
                    except AttributeError:
                        hint = '' 
                    
                    hint = hint.replace("_",".").replace(" ", "\s")
                    possible_pokemon = []

                    pattern = re.compile(hint)
                    for poke in self.data.pokemon:
                        if (bool(pattern.match(poke))):
                            possible_pokemon.append(poke)

                    for poke in possible_pokemon:     
                        time.sleep(1.5)
                        await message.channel.send("p!c " + poke)
                        caught_message = await self.wait_for('message', timeout=10, check=lambda m: check_caught(m))
                        if "you caught a" in caught_message.content.lower():
                            cprint("caught " + poke, "green")
                            return
                        else:
                            cprint("WRONG: not " + poke, "red")