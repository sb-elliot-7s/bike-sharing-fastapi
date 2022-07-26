from bson import ObjectId
from .schemas import PaymentStatus
from .interfaces.trip_repository_interface import TripRepositoryInterface

from weather_service.weather_network_service import WeatherNetworkService

from database import client
from .utils import PrepareDocumentService, CalculatesService, \
    CheckWeatherService
from .logics.trip_logics import CommonTripService
from .logics.bike_logics import CommonBikeService
from .logics.station_logics import CommonStationService


class TripRepository(TripRepositoryInterface):
    def __init__(self, trip_collection, bike_collection, station_collection):
        self._station_collection = station_collection
        self._bike_collection = bike_collection
        self._trip_collection = trip_collection

    async def get_detail_trip(self, trip_id: str, user_id: str):
        return await self._trip_collection.find_one(
            filter={'_id': ObjectId(trip_id), 'user_id': user_id}
        )

    async def create_trip(
            self, bike_id: str, user_id: str,
            weather_service: WeatherNetworkService
    ):
        async with await client.start_session() as session:
            async with session.start_transaction():
                bike = await self._bike_collection.find_one(
                    filter={'_id': ObjectId(bike_id)}
                )
                station = await CommonStationService().get_and_update_station(
                    station_collection=self._station_collection,
                    station_id=bike['station_id'],
                    _update={
                        '$inc': {
                            'available_count_of_bicycles': -1
                        },
                        '$pull': {
                            'bicycles': {'_id': ObjectId(bike_id)}
                        }
                    }
                )
                await self._bike_collection \
                    .update_one(filter={'_id': ObjectId(bike_id)},
                                update={'$set': {'station_id': None}})
                weather = await CheckWeatherService().data(
                    station['address']['city'], weather_service)
                document = await PrepareDocumentService() \
                    .prepare_start_trip_document(bike_id=bike_id, bike=bike,
                                                 user_id=user_id,
                                                 weather=weather)
                return await self._trip_collection.insert_one(document=document)

    async def finish_trip(self, station_id: str, user_id: str,
                          weather_service: WeatherNetworkService):
        async with await client.start_session() as session:
            async with session.start_transaction():
                trip = await CommonTripService() \
                    .get_trip(self._trip_collection, user_id=user_id,
                              payment_status=PaymentStatus.UNPAID)
                bike = await CommonBikeService() \
                    .bike_update(self._bike_collection, bike_id=trip['bike_id'],
                                 station_id=station_id)
                end_time, travel_time = CalculatesService().calculate_datetime(
                    start_time=trip['start_time'])
                total_amount = CalculatesService().calculate_total_amount(
                    travel_time, trip['price_bike'])
                # from gps -> points
                points = []
                station = await CommonStationService().get_and_update_station(
                    station_collection=self._station_collection,
                    station_id=station_id,
                    _update={
                        '$inc': {
                            'available_count_of_bicycles': 1
                        },
                        '$push': {
                            'bicycles': bike
                        }
                    }
                )
                weather = await CheckWeatherService().data(
                    station['address']['city'], weather_service)
                doc = await PrepareDocumentService() \
                    .prepare_finish_trip_document(station_id=station_id,
                                                  end_time=end_time,
                                                  points=points,
                                                  travel_time=travel_time,
                                                  weather=weather,
                                                  total_amount=total_amount)
                return await self._trip_collection.find_one_and_update(
                    filter={'user_id': user_id,
                            'payment_status': PaymentStatus.UNPAID.value},
                    update={'$set': doc}, return_document=True)
