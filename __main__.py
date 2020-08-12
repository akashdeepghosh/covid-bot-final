import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import when_mentioned_or
from discord.utils import get
from discord.ext.commands import bot

bott = commands.Bot(command_prefix=when_mentioned_or(".."))
bott.remove_command("help")

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

@bott.event
async def on_ready():
    print("Ready")
    while True:
        await bott.change_presence(activity=discord.Game(f"serving covid data in {len(bott.guilds)} servers"))
        await asyncio.sleep(600)


async def find_channel(guild):
    for c in guild.text_channels:
        if not c.permissions_for(guild.me).send_messages:
            continue
        return c
    return None


@bott.event
async def on_guild_join(guild):
    channel = await find_channel(guild)
    if channel is None:
        return
    embed = discord.Embed(description=
                          "For detailed information about commands, type `..help`"
                          , color=discord.Color.gold())
    embed.set_author(name="Coronavirus Bot",
                     icon_url="https://imgur.com/GsCEnJO.jpg")
    embed.add_field(name="Prefix", value="`..` or `@mention`", inline=False)
    embed.add_field(name="Bot Invite Link",
                    value="[:envelope: Invite](https://discord.com/api/oauth2/authorize?client_id=647804652825477141&permissions=8&scope=bot)",
                    inline=True)

    embed.set_footer(text="Stay Safe and Healthy!")

    await channel.send(embed=embed)

    channel = bott.get_channel(628716139224105000)
    await channel.send(embed=discord.Embed(
        description=f"Joined server **{guild.name}** with **{len(guild.members)}** members | Total guilds {len(bott.guilds)}",
        color=discord.Color.green()))


@bott.event
async def on_guild_remove(guild):
    channel = bott.get_channel(628716139224105000)
    await channel.send(embed=discord.Embed(
        description=f"Left server **{guild.name}** with **{len(guild.members)}** members | Total guilds {len(bott.guilds)}",
        color=discord.Color.gold()))

@bott.command()
async def ping(ctx):
    await ctx.send(' 🏓 Pong! {0}s'.format(round(bott.latency, 3)))

@bott.command()
async def invite(ctx):
    embed = discord.Embed(color=discord.Color.gold())
    embed.set_author(name="Coronavirus Bot",
                     icon_url="https://imgur.com/GsCEnJO.jpg")
    embed.add_field(name="Prefix", value="`..` or `@mention`", inline=False)
    embed.add_field(name="Bot Invite Link",
                    value="[:envelope: Invite](https://discord.com/api/oauth2/authorize?client_id=647804652825477141&permissions=8&scope=bot)",
                    inline=True)

    embed.set_footer(text="Stay Safe and Healthy!")
    await ctx.send(embed=embed)


@bott.command()
async def help(ctx):

    desc = ""
    desc += "__General Commands__😷\n\n"
    desc += " `overall`\nGet Overall stats about Coronavirus\n\n"
    desc += " `top`\nGet top 10 affected countries\n\n"
    desc += " `stats <country name or short form>`\nGet statistics about a particular country and contains live image from Wikipedia. Don't use <>\n\n"
    desc += " `plot <country name or short form>`\nPlots both linear and logarithmic graphs for a particular country. Don't use <>\n\n"
    desc += " `hist <country name or short form>`\nGet past 6 days data for a particular country. Don't use <>\n\n\n"

    desc += "__India specific commands__\n\n"
    desc += " `ind stats`\nGet stats about a particular state/union-territory/city of India\n\n"
    desc += " `ind today`\nGet stats about new cases/deaths/recoveries in India today\n\n"
    desc += "__Invite Command__\n\n"
    desc += " `invite` Invite the bot to your server\n\n"

    embed=discord.Embed(description=desc, color=discord.Color.gold())
    embed.add_field(name="Prefix", value="`..` or `@mention`", inline=False)

    embed.set_author(name="Information About Commands")
    embed.set_footer(text="Stay safe and healthy!")
    embed.color=discord.Color.gold()

    await ctx.send(embed=embed)


@bott.event
async def on_message(message):
    if message.content == f"<@!647804652825477141>" or message.content == f"<@647804652825477141>":
        embed = discord.Embed(description=
                              "Thanks for inviting me to the server.\nFor detailed information about commands, type `..help` or `@mention`"
                              , color=discord.Color.gold())
        embed.set_author(name="Coronavirus Bot",
                         icon_url="https://imgur.com/GsCEnJO.jpg")
        embed.add_field(name="Prefix", value="`..` or `@mention`", inline=False)
        embed.add_field(name="Bot Invite Link",
                        value="[:envelope: Invite](https://discord.com/api/oauth2/authorize?client_id=647804652825477141&permissions=8&scope=bot)",
                        inline=True)

        embed.set_footer(text=random.choice(banner), icon_url=ctx.author.avatar_url)

        await message.channel.send(embed=embed)
    

    await bott.process_commands(message)


if __name__ == "__main__":
    try:
        bott.load_extension("bot")
        bott.load_extension("india")
    except Exception as e:
        print(f'Failed to load file')
        print(str(e))
    bott.run("NjQ3ODA0NjUyODI1NDc3MTQx.XdlBGA.p9b3V3JBz0qPn764z3k4laZttqk")
