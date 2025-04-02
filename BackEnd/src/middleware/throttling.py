from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time
import json

# Store request timestamps and counts for each IP
request_logs = {}

# Define request limit settings
MAX_REQUESTS = 10  # Number of requests allowed
WINDOW_SIZE = 60   # Time window in seconds
EXCLUDED_PATHS = ["/docs", "/redoc", "/openapi.json", "/"]  # Paths to exclude from throttling

class ThrottleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check if path should be excluded from throttling
        path = request.url.path
        if path in EXCLUDED_PATHS:
            return await call_next(request)
            
        client_ip = request.client.host  # Get client IP
        current_time = time.time()
        
        # Initialize or clean up old requests for this IP
        if client_ip not in request_logs:
            request_logs[client_ip] = []
        
        # Remove requests older than the window
        request_logs[client_ip] = [
            timestamp for timestamp in request_logs[client_ip] 
            if current_time - timestamp < WINDOW_SIZE
        ]
        
        # Check if too many requests
        if len(request_logs[client_ip]) >= MAX_REQUESTS:
            reset_time = request_logs[client_ip][0] + WINDOW_SIZE
            wait_time = int(reset_time - current_time)
            return Response(
                json.dumps({
                    "detail": f"Rate limit exceeded. Try again in {wait_time} seconds."
                }),
                status_code=429,
                media_type="application/json",
                headers={"Retry-After": str(wait_time)}
            )
        
        # Log this request time
        request_logs[client_ip].append(current_time)
        
        # Process the request
        response = await call_next(request)
        return response