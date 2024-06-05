import pathlib
import random

import discord
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_SECRET = os.getenv('CLIENT_SECRET')
SERVER_ID = int(os.getenv('SERVER_ID'))

intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

DEFAULT_MAP_POOL = ["Oregon", "Club House", "Consulate", "Bank", "Kanal", "Chalet", "Kafe Dostoyevsky", "Border",
                    "Skycraper", "Coastline", "Theme Park", "Villa", "Outback", "Emerald Plains", "Nighthaven Labs",
                    "Lair", "House", "Presidential Plane", "Favela", "Stadium Bravo"]

map_pool = DEFAULT_MAP_POOL.copy()


def global_map_pool_to_str():
    out = "```"
    for x, i in enumerate(map_pool):
        out += f"{x + 1} {i}\n"

    out += "```"
    return out


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=SERVER_ID))
    print(f'We have logged in as {client.user}')


@tree.command(name="pool", description="returns current used map-pool", guild=discord.Object(id=SERVER_ID))
async def get_pool(interaction):
    await interaction.response.defer()
    await interaction.followup.send(global_map_pool_to_str(), wait=True)


@tree.command(name="random", description="returns [number] random maps", guild=discord.Object(id=SERVER_ID))
@app_commands.describe(number="number of maps to return")
async def random_command(interaction, number: int):
    await interaction.response.defer()
    global map_pool

    if number > len(map_pool):
        await interaction.followup.send(f"There are only {len(map_pool)} Maps in the Pool", wait=True)
        return

    if number <= 0:
        await interaction.followup.send("Your Brain must be smoother than Quantum stabilized atom mirror", wait=True)
        return

    if number == len(map_pool):
        await interaction.followup.send("Bro wants to select all the Maps💀", wait=True)
        return

    selected_pool = set()
    while len(selected_pool) < number:
        selected_pool.add(random.choice(map_pool))

    map_pool = list(selected_pool)

    out = "```"
    for x, i in enumerate(selected_pool):
        out += f"{x + 1} {i}\n"

    out += "```"
    await interaction.followup.send(out, wait=True)


@tree.command(name="map_ban", description="bans one Map from Pool", guild=discord.Object(id=SERVER_ID))
@app_commands.describe(map_nmbr="number of Maps to return")
async def map_ban(interaction, map_nmbr: int):
    await interaction.response.defer()
    global map_pool

    if len(map_pool) <= 1:
        await interaction.followup.send(f"Selected Map: {map_pool[0]}", wait=True)
        return

    if map_nmbr > len(map_pool):
        await interaction.followup.send(f"There are only {len(map_pool)} Maps in the Pool...", wait=True)
        return

    if map_nmbr <= 0:
        await interaction.followup.send("0 and smaller is invalid...", wait=True)
        return

    map_pool.pop(map_nmbr - 1)
    if len(map_pool) > 1:
        await interaction.followup.send(global_map_pool_to_str(), wait=True)
    else:
        await interaction.followup.send(f"Selected Map: {map_pool[0]}", wait=True)


@tree.command(name="reset", description="resets Map Pool to default", guild=discord.Object(id=SERVER_ID))
async def reset(interaction):
    await interaction.response.defer()
    global map_pool
    map_pool = DEFAULT_MAP_POOL.copy()
    await interaction.followup.send("Map Pool is now the default Map Pool", wait=True)

client.run(CLIENT_SECRET)
