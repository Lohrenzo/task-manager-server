from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from upstash_redis import Redis
from upstash_ratelimit import Ratelimit, FixedWindow
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Redis from environment
redis = Redis(
    url=os.getenv("UPSTASH_REDIS_REST_URL"),
    token=os.getenv("UPSTASH_REDIS_REST_TOKEN"),
)

# Configure rate limiter: 60 requests per minute per IP
limiter = Ratelimit(
    redis=redis, limiter=FixedWindow(max_requests=60, window=60), prefix="ratelimit"
)


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Use client IP as identifier
        identifier = request.client.host

        # Check rate limit
        result = limiter.limit(identifier)
        if not result.allowed:
            print(f"Rate limit exceeded for `{identifier}`.")
            raise HTTPException(status_code=429, detail="Rate limit exceeded.")

        # Proceed to next middleware / route
        response = await call_next(request)
        return response
