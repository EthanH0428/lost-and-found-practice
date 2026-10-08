from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import Settings, get_settings
from app.db.session import create_database_engine, create_session_factory, initialize_database


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    engine = create_database_engine(settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        initialize_database(engine)
        yield
        engine.dispose()

    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="교내에서 접수된 분실물을 등록하고 조회하는 API입니다.",
        debug=settings.debug,
        lifespan=lifespan,
    )
    application.state.session_factory = create_session_factory(engine)
    application.include_router(api_router, prefix=settings.api_v1_prefix)

    @application.get("/health", tags=["system"])
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()
