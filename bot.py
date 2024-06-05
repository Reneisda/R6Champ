import pathlib
import random

import discord
from discord import app_commands
import os

# .env file is buggy with python-dotenv
with open("secret.env", "r") as source:
    secrets = source.read().split("\n")

client_secret = secrets[0]
server_id = secrets[1]

print(client_secret)
intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

default_map_pool = ["Oregon", "Club House", "Consulate", "Bank", "Kanal", "Chalet", "Kafe Dostoyevsky", "Border",
                    "Skycraper", "Coastline", "Theme Park", "Villa", "Outback", "Emerald Plains", "Nighthaven Labs",
                    "Lair", "House", "Presidential Plane", "Favela", "Stadium Bravo"]

map_pool = default_map_pool.copy()


def global_map_pool_to_str():
    out = "```"
    for x, i in enumerate(map_pool):
        out += f"{x + 1} {i}\n"

    out += "```"
    return out


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=server_id))
    print(f'We have logged in as {client.user}')


@tree.command(name="pool", description="returns current used map-pool", guild=discord.Object(id=server_id))
async def first_command(interaction):
    await interaction.response.send_message(global_map_pool_to_str())


@tree.command(name="random", description="returns [number] random maps", guild=discord.Object(id=server_id))
@app_commands.describe(number="number of maps to return")
async def random_command(interaction, number: int):
    global map_pool

    if number > len(map_pool):
        await interaction.response.send_message(f"There are only {len(map_pool)} Maps in the Pool")
        return

    if number <= 0:
        await interaction.response.send_message(f"Your Brain must be smoother than Quantum stabilized atom mirror")
        return

    if number == len(map_pool):
        await interaction.response.send_message(f"Bro wants to select all the Maps💀")
        return

    selected_pool = set()
    while len(selected_pool) < number:
        selected_pool.add(random.choice(map_pool))

    map_pool = list(selected_pool)

    out = "```"
    for x, i in enumerate(selected_pool):
        out += f"{x + 1} {i}\n"

    out += "```"
    await interaction.response.send_message(out)


@tree.command(name="map_ban", description="bans one Map from Pool", guild=discord.Object(id=server_id))
@app_commands.describe(map_nmbr="number of Maps to return")
async def map_ban(interaction, map_nmbr: int):
    global map_pool

    if len(map_pool) <= 1:
        await interaction.response.send_message(f"Selected Map: {map_pool[0]}")
        return

    if map_nmbr > len(map_pool):
        await interaction.response.send_message(f"There are only {len(map_pool)} Maps in the Pool...")
        return

    if map_nmbr <= 0:
        await interaction.response.send_message("0 and smaller is invalid...")
        return

    map_pool.pop(map_nmbr - 1)
    if len(map_pool) > 1:
        await interaction.response.send_message(global_map_pool_to_str())
    else:
        await interaction.response.send_message(f"Selected Map: {map_pool[0]}")


@tree.command(name="reset", description="resets Map Pool to default", guild=discord.Object(id=server_id))
async def reset(interaction):
    global map_pool
    map_pool = default_map_pool
    await interaction.response.send_message("Map Pool is now the default Map Pool")

client.run(client_secret)
