from fastapi import APIRouter
from .endpoints import trading, prices, sso, sisensesso

router = APIRouter()

# Commenting out routes
# router.include_router(trading.router, tags=["Trading Signals"])
# router.include_router(prices.router, tags=["Prices"])

router.include_router(sso.router, tags=["sso"])
router.include_router(sisensesso.router, tags=["sisensesso"])
