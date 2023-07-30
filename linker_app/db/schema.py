from enum import Enum

# from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.sql import func
from flask_sqlalchemy.model import Model
from sqlalchemy import (
    MetaData,
    Column,
    Table,
    ForeignKey,
    # Enum as PgEnum,
    Integer,
    String,
    UUID,
    JSON,
    LargeBinary,
    DateTime,
    Boolean,
)

from linker_app.utils.db import get_str_uuid4

convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}
metadata = MetaData(naming_convention=convention)


class BaseModel(Model):
    pass


class EventType(Enum):
    STATUS_CHANGED = "status_changed"
    RESOURCE_ADDED = "resource_added"
    RESOURCE_DELETED = "resource_deleted"
    PHOTO_ADDED = "photo_added"


links_table = Table(
    "links",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("uuid", UUID, default=get_str_uuid4, index=True),
    Column("full_url", String(255), nullable=False, unique=True, index=True),
    Column("protocol", String(16), nullable=False),
    Column("domain", String, nullable=False),
    Column("domain_zone", String, nullable=False, index=True),
    Column("path", String(255)),
    Column("query_params", JSON),
    Column("unavailable_count", Integer, default=0),
    # Column("screenshot", LargeBinary, nullable=True),
)

links_screenshot = Table(
    "links_screenshots",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("link_id", Integer, ForeignKey("links.id")),
    Column("screenshot", LargeBinary, nullable=True),
)

response_table = Table(
    "link_responses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("link_id", Integer, ForeignKey("links.id")),
    Column("status_code", Integer, nullable=True),
    Column("request_time", DateTime(timezone=True), server_default=func.now()),
    Column("is_available", Boolean),
)

# file_processing_requests = Table(
#     "file_processing_requests",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("total_urls", Integer, nullable=True, default=None),
#     Column("processed_urls", Integer, nullable=True, default=None),
#     Column("errors", Integer, nullable=True, default=None),
#     Column("is_finished", Boolean, default=False),
# )

# news_feed_items = Table(
#     "news_feed_items",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("event_type", PgEnum(EventType, name="event_type"), nullable=False),
#     Column("resource_id", Integer, ForeignKey("web_resources.id")),
#     Column("timestamp", DateTime(timezone=True), server_default=func.now()),
# )
