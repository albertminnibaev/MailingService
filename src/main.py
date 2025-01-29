from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.config import settings
# from src.includes.logging import register_errors
from src.mailing.router import router as mailing_router


app = FastAPI(
    title="Mailing Service",
    description="Mailing Service",
)


app.mount('/static', StaticFiles(directory=(settings.BASE_DIR / 'static')), name='static')

# register_errors(app)

app.include_router(mailing_router)
