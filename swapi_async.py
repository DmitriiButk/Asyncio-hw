import asyncio
import aiohttp
import datetime
from more_itertools import chunked
from models import init_db, SwapiPeopleModel, engine, Session


MAX_CHUNK = 10
MAX_COUNT = 85


async def get_person(client: aiohttp.ClientSession, person_id: int):
    http_response = await client.get(f'https://swapi.dev/api/people/{person_id}')
    json_result = await http_response.json()
    return json_result


async def get_data(list_of_urls: list, value: str, client: aiohttp.ClientSession):
    some_list = []
    for url in list_of_urls:
        response = await client.get(url)
        data = await response.json()
        some_list.append(data[value])
    return ', '.join(some_list)


async def insert_to_db(client: aiohttp.ClientSession, list_of_jsons: list):
    async with Session() as session:
        for person in list_of_jsons:
            if person != {'detail': 'Not found'}:
                films = await get_data(list_of_urls=person['films'], value='title', client=client)
                species = await get_data(list_of_urls=person['species'], value='name', client=client)
                starships = await get_data(list_of_urls=person['starships'], value='name', client=client)
                vehicles = await get_data(list_of_urls=person['vehicles'], value='name', client=client)
                person = SwapiPeopleModel(
                    films=films,
                    species=species,
                    starships=starships,
                    vehicles=vehicles,
                    birth_year=person['birth_year'],
                    eye_color=person['eye_color'],
                    gender=person['gender'],
                    hair_color=person['hair_color'],
                    height=person['height'],
                    homeworld=person['homeworld'],
                    mass=person['mass'],
                    name=person['name'],
                    skin_color=person['skin_color']
                )
                session.add(person)
                await session.commit()


async def main():
    await init_db()
    client = aiohttp.ClientSession()
    for chunk in chunked(range(1, MAX_COUNT), MAX_CHUNK):
        people = [get_person(client=client, person_id=person_id) for person_id in chunk]
        result = await asyncio.gather(*people)
        asyncio.create_task(insert_to_db(client=client, list_of_jsons=result))
    tasks_set = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*tasks_set)
    await client.close()
    await engine.dispose()


if __name__ == '__main__':
    print('Start of program...wait.')
    start_time = datetime.datetime.now()
    asyncio.run(main())
    print(f'Program execution time: {datetime.datetime.now() - start_time}')
    print('End of program.')
