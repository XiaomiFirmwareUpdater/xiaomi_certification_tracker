"""Xiaomi Certification Tracker Database initialization"""
import logging

from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Connection, Engine

logger = logging.getLogger(__name__)
engine: Engine = create_engine(get_project_settings().get("CONNECTION_STRING"),
                               connect_args={'check_same_thread': False})
logger.info(f"Connected to {engine.name} database at {engine.url}")
connection: Connection = engine.connect()

# Create a MetaData instance
metadata: MetaData = MetaData()
# reflect db schema to MetaData
metadata.reflect(bind=engine)
