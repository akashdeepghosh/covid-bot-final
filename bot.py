import urllib

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
import re
import requests

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

async def send_error(ctx, message):
    await ctx.send(embed=Embed(description=f"{message}", color=Color.gold()))



def get_url_images_in_text(country):
    '''finds image urls'''
    country.replace(" ", "_")
    resp = requests.get(f"https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_{country}")
    text = resp.text
    urls = []
    results = re.findall(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpg)', text)
    for x in results:
      urls.append(x)
    if len(urls[0]) < 300:
        return urls[0]

    country = "the_"+country
    resp = requests.get(f"https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_{country}")
    text = resp.text
    urls = []
    results = re.findall(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpg)', text)
    for x in results:
        urls.append(x)
    if len(urls[0]) < 300:
        return urls[0]

    return None


async def plot_graph1(ctx, iso3, num, name):
    data = await api_covid.CovidAPI().get_country_timeline1(iso3)
    if data is None:
        await send_error(ctx, "API Error!")
        return
    x_axis = []
    cases = []
    deaths = []
    recovery = []
    for x in data['result']:
        try:
            x_axis.append(datetime.strptime(str(x), '%Y-%m-%d'))
            cases.append(data['result'][x]['confirmed'])
            deaths.append(data['result'][x]['deaths'])
            recovery.append(data['result'][x]['recovered'])
        except Exception:
            pass
    plt.plot(x_axis, cases, color='gold', linestyle='-', marker='o', markersize=4, markerfacecolor='gold', label="Total Cases")
    plt.plot(x_axis, recovery, color='green', linestyle='-', marker='o', markersize=4, markerfacecolor='green', label="Total Recoveries")
    plt.plot(x_axis, deaths, color='red', linestyle='-', marker='o', markersize=4, markerfacecolor='red', label="Total Deaths")

    plt.gcf().autofmt_xdate()
    plt.legend()
    ax = plt.axes()
    plt.setp(ax.get_xticklabels(), color="white")
    plt.setp(ax.get_yticklabels(), color="white")
    filename = "%s.png" % str(ctx.message.id)
    plt.savefig(filename, transparent=True)
    with open(filename, 'rb') as file:
        discord_file = File(BytesIO(file.read()), filename='plot.png')
    os.remove(filename)
    plt.clf()
    plt.close()
    embed = Embed(title=f"Linear graph for {name}", color=Color.gold())
    embed.set_image(url="attachment://plot.png")
    embed.set_footer(text=random.choice(banner), icon_url=ctx.author.avatar_url)
    if num == -1:
        return discord_file

    await ctx.channel.send(embed=embed, file=discord_file)
    if num == 0:
        return

    plt.plot(x_axis, cases, color='gold', linestyle='-', marker='o', markersize=4, markerfacecolor='gold',
             label="Total Cases")
    plt.plot(x_axis, recovery, color='green', linestyle='-', marker='o', markersize=4, markerfacecolor='green',
             label="Total Recoveries")
    plt.plot(x_axis, deaths, color='red', linestyle='-', marker='o', markersize=4, markerfacecolor='red',
             label="Total Deaths")

    plt.gcf().autofmt_xdate()
    plt.legend()
    ax = plt.axes()
    ax.set_yscale('log')
    plt.setp(ax.get_xticklabels(), color="white")
    plt.setp(ax.get_yticklabels(), color="white")
    filename = "%s.png" % str(ctx.message.id)
    plt.savefig(filename, transparent=True)
    with open(filename, 'rb') as file:
        discord_file = File(BytesIO(file.read()), filename='plot.png')
    os.remove(filename)
    plt.clf()
    plt.close()
    embed = Embed(title=f"Logarithmic graph for {name}",
                  color=Color.gold())
    embed.set_image(url="attachment://plot.png")

    embed.set_footer(text=random.choice(banner), icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed, file=discord_file)


# async def plot_graph2(ctx, iso3, name):
#     data = await api_covid.CovidAPI().get_country_timeline1(iso3[0])
#     if data is None:
#         await send_error(ctx, "API Error, take rest.")
#         return
#     x_axis = []
#     cases = []
#     for x in data['result']:
#         try:
#             x_axis.append(datetime.strptime(str(x), '%Y-%m-%d'))
#         except Exception:
#             pass
#     for x in iso3:
#         data = await api_covid.CovidAPI().get_country_timeline1(x)
#         if data is None:
#             await send_error(ctx, "API Error, stay strong during this pandemic.")
#             return
#         arr = []
#         for y in data['result']:
#             try:
#                 arr.append(data['result'][y]['confirmed'])
#             except Exception:
#                 pass
#         cases.append(arr)
#     col = ["red", "orange", "green", "blue", "gold"]
#     for i in range(0, len(iso3)):
#         plt.plot(x_axis, cases[i], color=col[i], linestyle='-', marker='o', markersize=4, markerfacecolor=col[i],
#                  label=name[i])

#     plt.gcf().autofmt_xdate()
#     plt.legend()
#     ax = plt.axes()
#     plt.setp(ax.get_xticklabels(), color="white")
#     plt.setp(ax.get_yticklabels(), color="white")
#     filename = "%s.png" % str(ctx.message.id)
#     plt.savefig(filename, transparent=True)
#     with open(filename, 'rb') as file:
#         discord_file = File(BytesIO(file.read()), filename='plot.png')
#     os.remove(filename)
#     plt.clf()
#     plt.close()
#     embed = Embed(title=f"Linear graph for {name}", color=Color.gold())
#     embed.set_image(url="attachment://plot.png")
#     embed.set_footer(text=random.choice(banner), icon_url=ctx.author.avatar_url)

#     await ctx.channel.send(embed=embed, file=discord_file)


async def plot_graph(ctx, iso2, num):
    data = await api_covid.CovidAPI().get_country_timeline(iso2)
    if data is None:
        await send_error(ctx, "API Error!")
        return
    x_axis = []
    cases = []
    deaths = []
    recovery = []
    for x in data['timelineitems'][0]:
        try:
            x_axis.append(datetime.strptime(str(x), '%m/%d/%y'))
            cases.append(data['timelineitems'][0][x]['total_cases'])
            deaths.append(data['timelineitems'][0][x]['total_deaths'])
            recovery.append(data['timelineitems'][0][x]['total_recoveries'])
        except Exception:
            pass
    plt.plot(x_axis, cases, color='gold', linestyle='-', marker='o', markersize=4, markerfacecolor='gold', label="Total Cases")
    plt.plot(x_axis, recovery, color='green', linestyle='-', marker='o', markersize=4, markerfacecolor='green', label="Total Recoveries")
    plt.plot(x_axis, deaths, color='red', linestyle='-', marker='o', markersize=4, markerfacecolor='red', label="Total Deaths")

    plt.gcf().autofmt_xdate()
    plt.legend()
    ax = plt.axes()
    plt.setp(ax.get_xticklabels(), color="white")
    plt.setp(ax.get_yticklabels(), color="white")
    filename = "%s.png" % str(ctx.message.id)
    plt.savefig(filename, transparent=True)
    with open(filename, 'rb') as file:
        discord_file = File(BytesIO(file.read()), filename='plot.png')
    os.remove(filename)
    plt.clf()
    plt.close()
    embed = Embed(title=f"Linear graph for {data['countrytimelinedata'][0]['info']['title']}", color=Color.gold())
    embed.set_image(url="attachment://plot.png")
    embed.set_footer(text=random.choice(banner), icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed, file=discord_file)
    if num == 0:
        return

    plt.plot(x_axis, cases, color='gold', linestyle='-', marker='o', markersize=4, markerfacecolor='gold',
             label="Total Cases")
    plt.plot(x_axis, recovery, color='green', linestyle='-', marker='o', markersize=4, markerfacecolor='green',
             label="Total Recoveries")
    plt.plot(x_axis, deaths, color='red', linestyle='-', marker='o', markersize=4, markerfacecolor='red',
             label="Total Deaths")

    plt.gcf().autofmt_xdate()
    plt.legend()
    ax = plt.axes()
    ax.set_yscale('log')
    plt.setp(ax.get_xticklabels(), color="white")
    plt.setp(ax.get_yticklabels(), color="white")
    filename = "%s.png" % str(ctx.message.id)
    plt.savefig(filename, transparent=True)
    with open(filename, 'rb') as file:
        discord_file = File(BytesIO(file.read()), filename='plot.png')
    os.remove(filename)
    plt.clf()
    plt.close()
    embed = Embed(title=f"Logarithmic graph for {data['countrytimelinedata'][0]['info']['title']}",
                  color=Color.gold())
    embed.set_image(url="attachment://plot.png")
    embed.set_footer(text=random.choice(banner), icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed, file=discord_file)


class Tracker(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.covid = api_covid.CovidAPI()

    def embed(self, text, color=None):
        color=Color.gold()
        return Embed(description=text, color=color)

    @commands.command(brief='Plot various graphs about a country')
    async def plot(self, ctx, *, country:str = None):
        """Usage: `..plot <country 2/3 digit code>` or `..plot <country_name>`"""
        
        if country is None:
            await ctx.send(f"Usage: `..plot <country 2/3 digit code>` or `..plot <country_name>`")
            return
        iso2 = ""
        name = ""
        slug = ""

        if len(country) == 3:
            try:
                country = await self.covid.iso3_to_iso2(country.lower())
            except Exception:
                pass

        data = await self.covid.get_countries_list()
        if data is None:
            await send_error(ctx, "API Error!")
            return

        if country.upper() == "IRAN":
            country = "ir"
        if country.upper() == "RUSSIA":
            country = "ru"

        for x in data:
            try:
                if x['Country'].upper() == country.upper() or x['ISO2'] == country.upper():
                    iso2 = x['ISO2']
                    name = x['Country']
                    slug = x['Slug']
                    break
            except Exception:
                pass

        if len(iso2) == 0:
            await send_error(ctx, "Please enter a valid Country Name or ISO2 or ISO3 code")
            return
        if iso2.lower() == "ir":
            name = "Iran"
        if iso2.lower() == "ru":
            name = "Russia"
        iso3 = await self.covid.iso2_to_iso3(iso2)

     #  await plot_graph(ctx, iso2, 1)
        await plot_graph1(ctx,iso3,1, name)

    @commands.command(brief="Get cases about any country")
    async def cases(self, ctx, *, country:str = None):
        """Usage: `..cases <country 2/3 digit code>` or `..cases <country_name>`"""

        if country is None:
            await ctx.send(f"Usage: `..cases <country 2/3 digit code>` or `..cases <country_name>`")
            return

        iso2 = ""
        name = ""
        slug = ""

        if len(country) == 3:
            country = await self.covid.iso3_to_iso2(country.lower())

        data = await self.covid.get_countries_list()
        if data is None:
            await send_error(ctx, "API Error!")
            return

        if country.upper() == "IRAN":
            country = "ir"
        if country.upper() == "RUSSIA":
            country = "ru"

        for x in data:
            try:
                if x['Country'].upper() == country.upper() or x['ISO2'] == country.upper():
                    iso2 = x['ISO2']
                    name = x['Country']
                    slug = x['Slug']
                    break
            except Exception:
                pass

        if len(iso2) == 0:
            await send_error(ctx, "Please enter a valid Country Name or ISO2 or ISO3 code")
            return

        if iso2.lower() == "ir":
            name = "Iran"
        if iso2.lower() == "ru":
            name = "Russia"

        data = await self.covid.get_country_data(iso2)
        tme = round(time.time())
        tme -= data['updated']
        hrs = int(tme / 3600)
        tme = tme % 3600
        min = int(tme / 60)
        tme = tme % 60
        hrs = max(hrs, 0)
        min = max(min, 0)
        update = f"Updated {hrs} hours {min} minutes and {tme} seconds ago\n{random.choice(banner)}"
        embed = discord.Embed(color=Color.gold())
        embed.set_author(name=f"Data for {name}", icon_url=data['countryInfo']['flag'])
        embed.set_thumbnail(url=data['countryInfo']['flag'])
        embed.add_field(name="Total Cases", value=f"{data['cases']} (+{data['todayCases']})", inline=False)
        embed.add_field(name="Total Deaths", value=f"{data['deaths']} (+{data['todayDeaths']})", inline=False)
        embed.add_field(name="Total Recoveries", value=f"{data['recovered']}", inline=False)
        embed.add_field(name="Active", value=str(data['active']), inline=True)
        embed.add_field(name="Critical", value=str(data['critical']), inline=True)
        embed.add_field(name="Tests Conducted", value=str(data['tests']), inline=True)
        embed.set_footer(text=update)


        iso3 = await self.covid.iso2_to_iso3(iso2)


        await ctx.send(embed=embed)



    @commands.command(brief="Overall Stats about Covid-19")
    async def overall(self, ctx, *, country: str = None):

        data = await self.covid.get_overall_data()
        if data is None:
            await send_error(ctx, "API Error!")
            return

        tme = round(time.time())
        tme -= data['updated']
        hrs = int(tme / 3600)
        tme = tme % 3600
        min = int(tme / 60)
        tme = tme % 60
        hrs = max(hrs, 0)
        min = max(min, 0)
        update = f"Updated {hrs} hours {min} minutes and {tme} seconds ago\n{random.choice(banner)}"

        embed = Embed(colour=Color.gold())
        embed.set_author(name="Overall Stats about Covid-19", icon_url="https://imgur.com/GsCEnJO.jpg")
        embed.add_field(name="Total Cases", value=str(data["cases"])+f" (+{data['todayCases']})", inline=False)
        embed.add_field(name="Total Deaths", value=str(data["deaths"])+f" (+{data['todayDeaths']})", inline=False)
        embed.add_field(name="Total Recoveries", value=str(data["recovered"]), inline=False)
        embed.add_field(name="Active Cases", value=str(data["active"]), inline=False)
        embed.add_field(name="Critical Cases", value=str(data["critical"]), inline=False)
        embed.add_field(name="Affected Countries", value=str(data["affectedCountries"]), inline=False)

        embed.set_footer(text=update)

        await ctx.send(embed=embed)

    @commands.command(bried="Worst affected countries")
    async def top(self,ctx):
        data = await self.covid.get_all_countries_data()
        if data is None:
            await send_error(ctx, "API Error!")
            return
        data = sorted(data, key=lambda i: i['cases'], reverse=True)

        data1 = []
        i = 0
        name, cases, death = "", "", ""
        for x in data:
            if i == 10:
                break
            name += f"\n:flag_{x['countryInfo']['iso2'].lower()}: {x['country']}"
            cases += f"\n{x['cases']} (+{x['todayCases']})"
            death += f"\n{x['deaths']} (+{x['todayDeaths']})"
            data1.append([name, cases, death])
            i += 1
        embed = Embed(colour=Color.gold())
        embed.set_author(name="Worst affected countries",
                         icon_url="https://imgur.com/GsCEnJO.jpg")

        embed.add_field(name="Country", value=name, inline=True)
        embed.add_field(name="Total Cases", value=cases, inline=True)
        embed.add_field(name="Total Deaths", value=death, inline=True)

        await ctx.send(embed=embed)


    @commands.command(brief='Plot stats about last 6 days')
    async def hist(self, ctx, *, country: str = None):
        """Usage: `..hist <country 2/3 digit code>` or `..hist <country_name>`"""

        if country is None:
            await ctx.send(f"Usage: `..hist <country 2/3 digit code>` or `..hist <country_name>`")
            return
        iso2 = ""
        name = ""
        slug = ""

        if len(country) == 3:
            try:
                country = await self.covid.iso3_to_iso2(country.lower())
            except Exception:
                pass

        data = await self.covid.get_countries_list()
        if data is None:
            await send_error(ctx, "API Error!")
            return

        if country.upper() == "IRAN":
            country = "ir"
        if country.upper() == "RUSSIA":
            country = "ru"

        for x in data:
            try:
                if x['Country'].upper() == country.upper() or x['ISO2'] == country.upper():
                    iso2 = x['ISO2']
                    name = x['Country']
                    slug = x['Slug']
                    break
            except Exception:
                pass

        if len(iso2) == 0:
            await send_error(ctx, "Please enter a valid Country Name or ISO2 or ISO3 code")
            return
        if iso2.lower() == "ir":
            name = "Iran"
        if iso2.lower() == "ru":
            name = "Russia"
        iso3 = await self.covid.iso2_to_iso3(iso2)
        data = await self.covid.get_country_timeline1(iso3)
        if data is None:
            await send_error(ctx, "API Error, do NOT panic.")
            return

        data = data['result']
        dates = []
        val = []
        for x in data:
            dates.append(x)
            val.append([data[x]['confirmed'], data[x]['deaths'], data[x]['recovered']])

        dates.reverse()
        val.reverse()
        val = [val[i] for i in range(0, 7)]
        dates = [dates[i] for i in range(0, 7)]
        dates = [datetime.strptime(x, '%Y-%m-%d').strftime('%d %b') for x in dates]

        embed = discord.Embed(color=Color.gold())
        embed.set_footer(text=random.choice(banner), icon_url=ctx.author.avatar_url)
        embed.set_author(name=f"Last 6 days Data for the country {name}", icon_url=f"https://corona.lmao.ninja/assets/img/flags/{iso2.lower()}.png")
        for i in range(0, 6):
            embed.add_field(name=f":calendar_spiral: {dates[i]}", value=f"Tot: {val[i][0]} \n`(+{val[i][0]-val[i+1][0]})`\nDead: {val[i][1]} \n`(+{val[i][1]-val[i+1][1]})`\nRec: {val[i][2]} \n`(+{val[i][2]-val[i+1][2]})`\n")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Tracker(client))
