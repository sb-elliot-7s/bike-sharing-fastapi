import uuid


class BikeRepository:
    def __init__(self, bike_collection):
        self._bike_collection = bike_collection

    async def create_bike(self):
        """
            bike_serial: UUID
            station_id: str
            brand: str
            model: str
            color: str
            bike_manufacturer: Optional[str]
            rent_price: float
        :return:
        """
        u = str(uuid.uuid4())
        print(u)
        document = {
            'bike_serial': u,
            'station_id': 'hello world',
            'brand': 'bmw',
            'model': 'xe',
            'color': 'red',
            'bike_manufacturer': 'germany',
            'rent_price': 100
        }
        await self._bike_collection.insert_one(document=document)
