from fastapi import HTTPException, status

from trip.schemas import PaymentStatus


class CommonTripService:
    @staticmethod
    async def get_trip(trip_collection, user_id: str, payment_status: PaymentStatus):
        if (trip := await trip_collection.find_one({'user_id': user_id,
                                                    'payment_status': payment_status.value})) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Trip not found')
        return trip
