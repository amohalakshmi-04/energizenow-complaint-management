from datetime import datetime
from models import db


class ServiceRequest(db.Model):
    __tablename__ = "service_requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="New"
    )

    priority = db.Column(
        db.String(20),
        nullable=False,
        default="Medium"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    resolution = db.Column(
        db.Text
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    assigned_to = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    def __repr__(self):
        return f"<ServiceRequest {self.id}: {self.title}>"