import discord
from gql import Client, gql

async def get_poke_japanese_name(pokeId, gql_client):
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

    result = await gql_client.execute(query, variable_values=params)
    print(result["pokemon_v2_pokemonspeciesname"][0]["name"])
    return result["pokemon_v2_pokemonspeciesname"][0]["name"]
