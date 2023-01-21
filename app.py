import asyncio
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm.session import close_all_sessions

from app.routers.index import router
from database.base import init_models
from parser.worker import background_parser

logger = logging.getLogger(__name__)


async def start_parser():
    # Инизиализация моделей SQLAlchemy
    await init_models()
    asyncio.create_task(background_parser())


def main():
    try:
        # Настраиваем логирование
        fmt_str = "BACKEND [%(asctime)s] - %(levelname)s - [%(module)s:%(lineno)s:%(funcName)s] - %(message)s"
        logging.basicConfig(level=logging.INFO, format=fmt_str)

        # Инизиализация роутеров, мидлварей и приложения
        app = FastAPI(title='Mera Capital Test', docs_url='/dev', on_startup=(start_parser,))
        app.include_router(router, tags=['Pnl'], prefix='/api')
        app.add_middleware(CORSMiddleware,
                           allow_origins=["http://localhost/", "http://localhost:8000", "http://localhost:3000"],
                           allow_credentials=True,
                           allow_methods=["*"],
                           allow_headers=["*"])

        # Запускаем сервер и указываем путь до конфига логов запросов
        uvicorn.run(app, host='127.0.0.1', port=8000, log_config='log.ini')
    except Exception as e:
        logger.warning(e)
    finally:
        close_all_sessions()


if __name__ == '__main__':
    main()
