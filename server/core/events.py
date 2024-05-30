# events.py
import asyncio

import aioredis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress
from rich.table import Table
from sqlalchemy import inspect
from starlette.routing import Route

from core.logging_config import setup_logging
from db.database_config import SessionLocal, engine

logger = setup_logging()
console = Console()
logger.add(RichHandler())


async def cache_hit(key):
    console.print(f"[green]Cache Hit:[/green] {key}")


async def cache_miss(key):
    console.print(f"[red]Cache Miss:[/red] {key}")


class CustomRedisBackend(RedisBackend):
    async def get(self, key):
        result = await super().get(key)
        if result is not None:
            await cache_hit(key)
        else:
            await cache_miss(key)
        return result


def create_start_app_handler(app: FastAPI):
    async def start_app() -> None:
        # Create a Redis connection pool
        redis = await aioredis.create_redis_pool("redis://localhost:6379/0")

        # Initialize the cache
        FastAPICache.init(CustomRedisBackend(redis), prefix="fastapi-cache")

        # Initialize a state object if it doesn't exist
        if not hasattr(app, "state"):
            app.state = type('', (), {})()

        # Connect to the database
        app.state.db = SessionLocal()

        # Log the name of the database and the tables in the database using Rich table
        database_name = engine.url.database
        table_names = inspect(engine).get_table_names()
        table = Table(title="Database Information")
        table.add_column("Database Name", style="cyan", justify="center")
        table.add_column("Tables", style="magenta", justify="center")
        table.add_row(database_name, "\n".join(table_names))
        console.print(table)

        # Log the routes
        console.print("[cyan]Routes:[/cyan]")
        for route in app.routes:
            if isinstance(route, Route):
                console.print(route.path)

        # Add progress bar for application startup
        console.print("\n[bold cyan]Starting Application...[/bold cyan]")
        with Progress() as progress:
            task_id = progress.add_task("[yellow]Initializing...", total=3)
            progress.advance(task_id)
            await asyncio.sleep(1)
            progress.advance(task_id)
            await asyncio.sleep(1)
            progress.advance(task_id)
            await asyncio.sleep(1)

        console.print("[bold green]Application Started Successfully![/bold green]")

    return start_app


def create_stop_app_handler(app: FastAPI):
    async def stop_app() -> None:
        # Disconnect from the database
        if hasattr(app, "state") and hasattr(app.state, "db"):
            app.state.db.close()
            console.print("[red]Disconnected from the database.[/red]")

    return stop_app
