from models import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="customer"
    )

    # Customer complaints
    complaints = db.relationship(
        "Complaint",
        backref="customer",
        lazy=True,
        foreign_keys="Complaint.customer_id"
    )

    # Complaints assigned to staff
    assigned_complaints = db.relationship(
        "Complaint",
        backref="assigned_staff",
        lazy=True,
        foreign_keys="Complaint.assigned_to"
    )

    def set_password(self, password):
        """Create a secure password hash."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check a password against the stored hash."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.email}>"