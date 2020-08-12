import discord
from discord.ext import commands
from discord import Embed, Color, File
from random import randint
import paginator
import api_covid
from operator import itemgetter
import matplotlib.pyplot as plt
from io import BytesIO
import os
from datetime import datetime
import json
import random
import time

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


states=["India", "Andaman and Nicobar Islands", "Andhra Pradesh", "Assam", "Bihar", "Chandigarh", "Chhattisgarh",
        "Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka",
        "Kerala", "Ladakh", "Madhya Pradesh", "Maharashtra", "Manipur", "Mizoram", "Odisha", "Puducherry", "Punjab",
        "Rajasthan", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"]

async def send_error(ctx, message):
    await ctx.send(embed=Embed(description=f"{message}",color=Color.gold()))


async def send_help(ctx):
    desc = "__Specific commands (INDIA)__\n\n"
    desc += "1. `..ind stats`\nGet stats about a particular state/union-territory/city of India\nEx: **..ind stats**\n\n"
    desc += "2. `..ind today`\nGet stats about new data in whole India today\nEx: **..ind today**\n\n\n"

    embed = discord.Embed(description=desc, color=discord.Color.orange())
    embed.set_author(name="Information About Commands")
    embed.add_field(name="Prefix", value="`..` or `@mention`", inline=False)


    await ctx.send(embed=embed)

class India(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.covid = api_covid.CovidAPI()
        self.states = states

    def embed(self, text, color=Color.gold()):
        color=Color.gold()
        return Embed(description=text, color=color)

    @commands.group(brief="Stats about all districts in India", invoke_without_command=True)
    async def ind(self, ctx):
        await send_help(ctx)

    @ind.command(brief='Get coronavirus stats for states/union territories')
    async def stats(self, ctx, choice: int = None):
        if choice is None:
            header = ["ID", "Region"]
            count = 0
            data = []
            for x in self.states:
                data.append([str(count), x])
                count += 1
            message = f"To get stats for a region, type `..ind stats <ID from table>`"
            await paginator.Paginator(data, header, "Select the region", 12, message).paginate(ctx, self.client)
            return

        if choice not in range(0, len(self.states)):
            await send_error(ctx, f"Please enter a valid integer between 0 and {len(self.states) - 1}")
            return

        if choice != 0:
            state = self.states[choice]
            district_data = await self.covid.get_district_data()
            if district_data is None:
                await send_error(ctx, "API Error, Meanwhile stay hydrated and wash your hands.!")
                return
            all_data = await self.covid.get_all_data()
            if all_data is None:
                await send_error(ctx, "API Error, Meanwhile don't touch your face when you're outside")
                return
            state_data = None
            for x in all_data["statewise"]:
                if x["state"] == state:
                    state_data = x
            data = []
            data.append([state_data["confirmed"], state_data["active"], state_data["deaths"], state_data["recovered"],
                         str(state_data["deltaconfirmed"]), str(state_data["deltadeaths"])])
            header = ["Total", "Active Cases", "Deaths", "Recovered", "Daily Cases", "New Deaths"]
            await paginator.Paginator(data, header, f"Data for the state of {state}", 10).paginate(ctx, self.client)

            data = []
            cnt = 0
            for x in district_data[state]["districtData"]:
                data.append([x, district_data[state]["districtData"][x]["confirmed"], district_data[state]["districtData"][x]["delta"]["confirmed"]])
            data = sorted(data, key=itemgetter(1), reverse=True)
            data = [[x[0], str(x[1]), str(x[2])] for x in data]
            header = ["District Name", "Total Cases", "New Cases"]
            await paginator.Paginator(data, header, f"District-wise data for the state of {state}", 10).paginate(ctx, self.client)
        else:
            all_data = await self.covid.get_all_data()
            if all_data is None:
                await send_error(ctx, "API Error, don't forget to stay hydrated.")
                return
            state = "Total"
            state_data = None
            for x in all_data["statewise"]:
                if x["state"] == state:
                    state_data = x
            data = []
            data.append([state_data["confirmed"], state_data["active"], state_data["deaths"], state_data["recovered"],
                         str(state_data["deltaconfirmed"]), str(state_data["deltadeaths"])])
            header = ["Total", "Active Cases", "Deaths", "Recovered", "New Cases", "New Deaths"]
            await paginator.Paginator(data, header, f"Data for India", 10).paginate(ctx, self.client)

            all_states_data = []
            for x in all_data["statewise"]:
                all_states_data.append([x["state"], int(x["confirmed"]), x["deltaconfirmed"], int(x["deaths"]), x["deltadeaths"]])
            all_states_data = sorted(all_states_data, key=itemgetter(1), reverse=True)
            data = [[x[0], str(x[1]), str(x[2]), str(x[3]), str(x[4])] for x in all_states_data]
            header = ["Region", "Total Cases", "New Cases", "Deaths", "New Deaths"]
            await paginator.Paginator(data, header, f"India", 10).paginate(ctx, self.client)

    @ind.command(brief='Stats about daily new cases')
    async def today(self, ctx):
        all_data = await self.covid.get_all_data()
        if all_data is None:
            await send_error(ctx, "API Error, do NOT go out unless absolutely necessary")
            return
        all_states_data = []
        for x in all_data["statewise"]:
            all_states_data.append(
                [x["state"], int(x["deltaconfirmed"]), int(x["deltadeaths"]), int(x["deltarecovered"])])
        all_states_data = sorted(all_states_data, key=itemgetter(1), reverse=True)
        data = [[x[0], str(x[1]), str(x[2]), str(x[3])] for x in all_states_data]
        header = ["Region", "New Cases", "New Deaths", "New Recoveries"]
        await paginator.Paginator(data, header, f"Data for India", 10).paginate(ctx, self.client)


def setup(client):
    client.add_cog(India(client))