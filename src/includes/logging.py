from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException

from http import HTTPStatus

from loguru import logger

from src.config import logging_settings


log_directory = logging_settings.log_dir
log_directory.mkdir(parents=True, exist_ok=True)

logger.remove()

logger.add(
    log_directory.joinpath('debug_{time}.log'),
    rotation='15 MB',
    format='{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}',
    encoding='utf-8',
    enqueue=True,
    level='DEBUG',
    compression='zip'
)


def register_errors(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_error_handler(
            request: Request,
            exc: HTTPException,
    ):
        """
        Логирование всех HTTPException
        """
        logger.opt(exception=True).warning(exc)
        content = {'detail': [
            {"msg": exc.detail}
        ]}
        return JSONResponse(
            status_code=exc.status_code,
            content=content
        )

    @app.exception_handler(Exception)
    async def error_handler(
            request: Request,
            exc: Exception,
    ):
        """
        Логирование всех Exception
        """
        logger.exception(exc)
        content = {'detail': [
            {"msg": HTTPStatus(500).phrase}
        ]}
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content=content,
        )

    @app.exception_handler(StarletteHTTPException)
    async def validation_error_handler(
            request: Request,
            exc: StarletteHTTPException,
    ):
        """
        Логирование всех StarletteHTTPException
        """
        content = {'detail': [
            {"msg": exc.detail}
        ]}
        logger.opt(exception=True).warning(exc)
        return JSONResponse(
            status_code=exc.status_code,
            content=content
        )
