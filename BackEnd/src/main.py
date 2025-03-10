from fastapi import FastAPI
from src.api.endpoints import basic,sentiment


app = FastAPI()

# Include Routers
app.include_router(basic.router, prefix='/basic', tags=['Basic NLP'])
# app.include_router(advanced.router, prefix='/advanced', tags=['Advanced NLP'])
app.include_router(sentiment.router, prefix='/sentiment', tags=['Sentiment Analysis'])
# app.include_router(visualization.router, prefix='/visualization', tags=['Text Visualization'])
# app.include_router(auth.router, prefix='/auth', tags=['Authentication'])
# app.include_router(users.router, prefix='/users', tags=['Users'])
# app.include_router(health.router, prefix='/health', tags=['Health'])

# ✅ Root Endpoint
@app.get("/", tags=["Root"])
def home():
    return {
        "message": "Welcome to Bhashasutra API",
        "status": "Running",
        "version": "1.0"
    }
    
# ✅ Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)

