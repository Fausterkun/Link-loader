import uuid

from linker_app import db


class Links(db.Model):
    """Model for present single link"""

    uuid = db.Column(db.UUID, default=uuid.uuid4, index=True)
    url = db.Column(db.String(255), nullable=False, unique=True, index=True)
    protocol = db.Column(db.String(16), nullable=False)
    domain = db.Column(db.String, nullable=False)
    domain_zone = db.Column(db.String, nullable=False, index=True)
    path = db.Column(db.String(255))
    params = db.Column(db.JSON)
    unavailable_times = db.Column(db.Integer, default=0)
