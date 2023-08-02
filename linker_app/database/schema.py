from enum import Enum
import uuid

# from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import declared_attr
from sqlalchemy import (
    MetaData,
    Column,
    Table,
    ForeignKey,
    Enum as PgEnum,
    Integer,
    String,
    UUID,
    JSON,
    LargeBinary,
    DateTime,
    Boolean,
)
from flask_sqlalchemy.model import Model

from linker_app.utils.db import get_str_uuid4

from linker_app import db


class EventType(Enum):
    STATUS_CHANGED = "status_changed"
    RESOURCE_ADDED = "resource_added"
    RESOURCE_DELETED = "resource_deleted"
    PHOTO_ADDED = "photo_added"


class Links(db.Model):
    """ Model for present single link """
    id = Column(Integer, primary_key=True)
    # uuid = Column(UUID, default=get_str_uuid4, index=True),
    uuid = Column(UUID, default=uuid.uuid4, index=True)
    url = Column(String(255), nullable=False, unique=True, index=True)
    protocol = Column(String(16), nullable=False)
    domain = Column(String, nullable=False)
    domain_zone = Column(String, nullable=False, index=True)
    path = Column(String(255))
    params = Column(JSON)
    unavailable_times = Column(Integer, default=0)

# links_table = Table(
#     "links",
#     metadata,
#     # Column("id", Integer, primary_key=True),
#     Column("uuid", UUID, default=get_str_uuid4, index=True),
#     Column("full_url", String(255), nullable=False, unique=True, index=True),
#     Column("protocol", String(16), nullable=False),
#     Column("domain", String, nullable=False),
#     Column("domain_zone", String, nullable=False, index=True),
#     Column("path", String(255)),
#     Column("params", JSON),
#     Column("unavailable_count", Integer, default=0),
#     # Column("screenshot", LargeBinary, nullable=True),
# )
#
# screenshot_table = Table(
#     "links_screenshots",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("link_id", Integer, ForeignKey("links.id")),
#     Column("screenshot", LargeBinary, nullable=True),
# )
#
# link_status_table = Table(
#     "link_status",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("link_id", Integer, ForeignKey("links.id")),
#     Column("status_code", Integer, nullable=True),
#     Column("request_time", DateTime(timezone=True), server_default=func.now()),
#     Column("is_available", Boolean),
# )
#
# file_parse_requests_table = Table(
#     "file_parse_requests",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, unique=True),
#     Column("total_urls", Integer, default=None),
#     Column("processed_urls", Integer, nullable=True, default=None),
#     Column("errors", Integer, nullable=True, default=None),
#     Column("is_finished", Boolean, default=False),
# )
