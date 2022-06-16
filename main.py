from fastapi import FastAPI
from bike.controllers import bike_router
from account.controllers import account_router
from address.controllers import address_router
from trip.controllers import trip_router

app = FastAPI(title='bike')

app.include_router(bike_router)
app.include_router(account_router)
app.include_router(address_router)
app.include_router(trip_router)
