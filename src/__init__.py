from fastapi import FastAPI

app = FastAPI()

# Import and register blueprints/modules
from src.modules.bot.bot_router import bot_router

app.include_router(bot_router)