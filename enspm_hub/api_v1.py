from ninja.throttling import AnonRateThrottle, AuthRateThrottle
from ninja import NinjaAPI
from core.api.auth import auth_router
from core.api.users import users_router


api_v1 = NinjaAPI(
    title="ENSPM Hub API V1",
    version="1.0.0",
    description="API V1 for ENSPM Hub",
    throttle=[
        AnonRateThrottle('10/s'),
        AuthRateThrottle('100/s')
    ]
)

# Inclusion des routers
api_v1.add_router("/auth/", auth_router)
api_v1.add_router("/users/", users_router)