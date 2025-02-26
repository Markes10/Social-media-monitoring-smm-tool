import asyncio
import uvicorn
from fastapi import FastAPI
from routes import social_media, sentiment, realtime
from twitter_fetcher import fetch_twitter_data
from facebook_fetcher import fetch_facebook_data

app = FastAPI(title="Social Media Monitoring API")

# Include routes
app.include_router(social_media.router, prefix="/api")
app.include_router(sentiment.router, prefix="/api")
app.include_router(realtime.router, prefix="/api")

# Run fetchers on startup
@app.on_event("startup")
async def start_fetchers():
    asyncio.create_task(fetch_twitter_data())
    asyncio.create_task(fetch_facebook_data())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
