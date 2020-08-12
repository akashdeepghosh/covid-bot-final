import asyncio
from math import ceil
from random import randint
from discord import Embed, Color
import json
import random

banner = ["🧴🤲 If soap is unavailable; use alcohol-based sanitizer",
		"🚫🤦 Don't touch your face",
		"✅🤧💪 Do sneeze into your elbow",
		"🧼🖐⏲  Wash your hands regularly",
		"🚇😷🛒 Wear a mask in public",
		"🚫🤝 No handshakes",
		"🚫🧑‍🤝‍🧑 No close contact",
		"🚫🏟 No large gatherings",
		"🧍↔️🧍 Keep a reasonable distance from others",
		"📦🚪 Ask agents to leave packages at door for no-contact delivery",
		"🧼👐💦 Wash your hands thoroughly for a minimum of 20 seconds",
		"🧍▫️▫️🧍 Stand 2m (6ft) apart"]



class Paginator:
    def __init__(self, data, headers, title, per_page=10, info:str=None):
        self.data = data
        self.title = title
        self.per_page = per_page
        self.headers = headers
        self.total_pages = ceil(len(self.data)/self.per_page)
        self.current_page = 1
        self.message = None
        self.info = info
        self.reactions = ["\U000025c0", "\U000025b6"]

    def get_page_elements(self, page_no):
        return self.data[(page_no-1)*self.per_page:page_no*self.per_page]

    def get_page_content(self, page_no):
        elements = self.get_page_elements(page_no)
        val = [0]*len(self.headers)
        for i in range(len(val)):
            val[i] = max(max([len(element[i]) for element in elements]), len(self.headers[i]))
        content, dashes = "", ""

        for i in range(len(val)):
            content += self.headers[i] + " "*(val[i] - len(self.headers[i])) + " "
            dashes += "-"*val[i] + " "

        content += "\n"+dashes+"\n"

        for i in range(len(elements)):
            for j in range(len(val)):
                content += elements[i][j] + " "*(val[j] - len(elements[i][j])) + " "
            content += "\n"
        return f"```\n{content}```"

    async def paginate(self, ctx, client):
        embed = Embed(title=self.title, description=self.get_page_content(self.current_page),
                      color=Color(randint(0, 0xFFFFFF)))
        embed.set_footer(text="Page %s out of %s\n%s" % (str(self.current_page), str(self.total_pages), random.choice(banner)))
        self.message = await ctx.channel.send(embed=embed)
        if self.total_pages == 1:
            return
        if self.info:
            await ctx.channel.send(self.info)
        await self.message.add_reaction(self.reactions[0])
        await self.message.add_reaction(self.reactions[1])

        def check(reaction, user):
            return reaction.message.id == self.message.id and reaction.emoji in self.reactions and user != client.user

        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=180, check=check)
                try:
                    await reaction.remove(user)
                except Exception:
                    pass
                if reaction.emoji == self.reactions[0]:
                    self.current_page -= 1
                    if self.current_page == 0:
                        self.current_page = self.total_pages
                    embed.description = self.get_page_content(self.current_page)
                    embed.set_footer(text="Page %s out of %s\n%s" % (str(self.current_page), str(self.total_pages), random.choice(banner)))
                    await self.message.edit(embed=embed)
                else:
                    self.current_page += 1
                    if self.current_page > self.total_pages:
                        self.current_page = 1
                    embed.description = self.get_page_content(self.current_page)
                    embed.set_footer(text="Page %s out of %s\n%s" % (str(self.current_page), str(self.total_pages), random.choice(banner)))
                    await self.message.edit(embed=embed)
            except asyncio.TimeoutError:
                await self.message.clear_reactions()
                break