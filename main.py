from fastapi import FastAPI
from bike.bike_controllers import bike_router
from bike.station_controllers import station_router
from account.controllers import account_router
from trip.controllers import trip_router
from payments_service.payment_controllers import payment_router

app = FastAPI(title='bike')

app.include_router(bike_router)
app.include_router(account_router)
app.include_router(trip_router)
app.include_router(station_router)
app.include_router(payment_router)
