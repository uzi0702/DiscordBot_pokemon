import imp
from inspect import trace
from tokenize import Double
import discord
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import json


transport = AIOHTTPTransport(url= "https://beta.pokeapi.co/graphql/v1beta")
gql_client = Client(transport=transport, fetch_schema_from_transport=True)

intents = discord.Intents.default()
intents.message_content = True

TOKEN = ""

discord_client = discord.Client(intents=intents)



@discord_client.event
async def on_ready():
    print(f"We have logged in as {discord_client.user}")

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    def check(msg):
        return msg.author == message.author

    if message.author.bot:
        return

    if message.content.startswith("!pokemon"):

        await message.channel.send("hello! Please input a height and weight")

        wait_message = await discord_client.wait_for("message",check=check)

        height, weight = wait_message.content.split()

        weight = int(weight)*10
        height = int(int(height) / 10)

        params={
            "weight": weight,
            "height": height,
        }

        query = gql(
            """
            query samplePokeAPIquery($weight: Int!, $height: Int!) {
            pokemon_v2_pokemon(limit: 10, where: {_and: {weight: {_eq: $weight}, height: {_eq: $height}}}) {
                height
                weight
                name
                id
            }
            }
        """
        )

        result =await gql_client.execute_async(query, variable_values=params)
        print(json.dumps(result, indent=2))

        await message.channel.send("height, weight, name, id")

        await message.channel.send(json.dumps(result, indent=2))

        pokeId = result["pokemon_v2_pokemon"][0]["id"]

        params = {
        "pokeId": pokeId
        }

        query = gql(
        """
        query getJapanesePokeName($pokeId: Int!) {
            pokemon_v2_pokemonspeciesname(where: {language_id: {_eq: 1}, pokemon_species_id: {_eq: $pokeId}}) {
            name
            }
        }
        """
        )

        ja_result = await gql_client.execute_async(query, variable_values=params)
        print(ja_result["pokemon_v2_pokemonspeciesname"][0]["name"])

        await message.channel.send(ja_result["pokemon_v2_pokemonspeciesname"][0]["name"])

discord_client.run(TOKEN)
