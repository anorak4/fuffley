from fastapi import APIRouter
from .endpoints import trading, prices

router = APIRouter()

# Commenting out routes
# router.include_router(trading.router, tags=["Trading Signals"])
# router.include_router(prices.router, tags=["Prices"])
