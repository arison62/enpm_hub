from ninja.throttling import AnonRateThrottle, AuthRateThrottle
from ninja import NinjaAPI

api_v1 = NinjaAPI(
    title="ENSPM Hub API V1",
    version="1.0.0",
    description="API V1 for ENSPM Hub",
    throttle=[
        AnonRateThrottle('10/s'),
        AuthRateThrottle('100/s')
    ]
)