from typing import Optional

import aiohttp
from configs import get_configs
from .schemas import WeatherSchema


class WeatherNetworkService:

    @staticmethod
    async def fetch_data(params: dict) -> Optional[WeatherSchema]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=get_configs().weather_url, params=params
            ) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                weather_data = {
                    'city': params.get('q'),
                    'temp': data.get('main').get('temp'),
                    'temp_min': data.get('main').get('temp_min'),
                    'temp_max': data.get('main').get('temp_max'),
                    'coord': {
                        'lon': data.get('coord').get('lon'),
                        'lat': data.get('coord').get('lat')
                    }
                }
                return WeatherSchema(**weather_data)
