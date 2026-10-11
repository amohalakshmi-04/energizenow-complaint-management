from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.user import User
from models.complaint import Complaint
from models.service_request import ServiceRequest
from models.category import Category