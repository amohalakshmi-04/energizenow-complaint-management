
import os

class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "complaints-service-management-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:@localhost/energizenow"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False