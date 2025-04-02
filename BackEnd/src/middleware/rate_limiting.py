# src/middleware/rate_limiting.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time
import json
from collections import defaultdict

# Store request counts per IP
request_counters = defaultdict(lambda: {"count": 0, "reset_time": 0})

# Define rate limit settings
RATE_LIMIT = 100  # requests
RATE_WINDOW = 3600  # seconds (1 hour)

# Paths to exclude from rate limiting
EXCLUDED_PATHS = ["/docs", "/redoc", "/openapi.json", "/"]

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for excluded paths
        path = request.url.path
        if path in EXCLUDED_PATHS:
            return await call_next(request)
            
        client_ip = request.client.host
        current_time = time.time()
        
        # Check if the time window has expired and reset if needed
        if current_time > request_counters[client_ip]["reset_time"]:
            request_counters[client_ip] = {
                "count": 0,
                "reset_time": current_time + RATE_WINDOW
            }
        
        # Increment request counter
        request_counters[client_ip]["count"] += 1
        
        # Check if rate limit exceeded
        if request_counters[client_ip]["count"] > RATE_LIMIT:
            reset_time = request_counters[client_ip]["reset_time"]
            wait_seconds = int(reset_time - current_time)
            
            remaining_minutes = wait_seconds // 60
            remaining_seconds = wait_seconds % 60
            
            time_message = (
                f"{remaining_minutes} minutes and {remaining_seconds} seconds" 
                if remaining_minutes > 0 
                else f"{remaining_seconds} seconds"
            )
            
            return Response(
                json.dumps({
                    "detail": f"Rate limit exceeded. Try again in {time_message}."
                }),
                status_code=429,
                media_type="application/json",
                headers={
                    "Retry-After": str(wait_seconds),
                    "X-RateLimit-Limit": str(RATE_LIMIT),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(reset_time))
                }
            )
        
        # Add rate limit headers to response
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = RATE_LIMIT - request_counters[client_ip]["count"]
        response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(request_counters[client_ip]["reset_time"]))
        
        return response