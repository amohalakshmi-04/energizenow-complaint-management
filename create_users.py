from app import app
from models import db
from models.user import User


with app.app_context():

    users = [
        {
            "name": "EnergizeNow Admin",
            "email": "admin@energizenow.com",
            "password": "Admin@123",
            "role": "admin"
        },
        {
            "name": "EnergizeNow Staff",
            "email": "staff@energizenow.com",
            "password": "Staff@123",
            "role": "staff"
        },
        {
            "name": "Demo Customer",
            "email": "customer@energizenow.com",
            "password": "Customer@123",
            "role": "customer"
        }
    ]

    for data in users:

        existing_user = User.query.filter_by(
            email=data["email"]
        ).first()

        if existing_user:
            existing_user.name = data["name"]
            existing_user.role = data["role"]
            existing_user.set_password(data["password"])

        else:
            user = User(
                name=data["name"],
                email=data["email"],
                role=data["role"]
            )

            user.set_password(data["password"])

            db.session.add(user)

    db.session.commit()

    print("Users created/updated successfully!")

    print("\nLogin credentials:")
    print("--------------------------------")
    print("ADMIN")
    print("Email: admin@energizenow.com")
    print("Password: Admin@123")

    print("\nSTAFF")
    print("Email: staff@energizenow.com")
    print("Password: Staff@123")

    print("\nCUSTOMER")
    print("Email: customer@energizenow.com")
    print("Password: Customer@123")