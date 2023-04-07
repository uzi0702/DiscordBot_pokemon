import discord
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import json
import os


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


        for i in range(len(result["pokemon_v2_pokemon"])):
            pokeId = result["pokemon_v2_pokemon"][i]["id"]
            ja_result = await get_poke_japanese_name(pokeId=pokeId)
            print(ja_result)
            await message.channel.send(ja_result)


async def get_poke_japanese_name(pokeId):
    """
    pokemon_species_id(整数)を指定すると、そのポケモンの日本語名を取得する
    """
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

    result = await gql_client.execute_async(query, variable_values=params)
    return result["pokemon_v2_pokemonspeciesname"][0]["name"]

discord_client.run(TOKEN)
