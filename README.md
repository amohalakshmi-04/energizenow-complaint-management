# EnergizeNow – Complaints & Service Management System

## 1. Project Overview

EnergizeNow is a web-based Complaints and Service Management System developed using Python Flask. The application helps manage customer complaints and service requests through a user-friendly web interface.

Customers can log in, submit complaints, and create service requests. Staff and administrators can manage complaint records, review service requests, and monitor their progress according to their assigned roles.

The application aims to improve customer service, simplify complaint tracking, and organize service-related information efficiently.

## 2. Objectives

- Provide an efficient system for managing customer complaints.
- Allow customers to submit service requests.
- Maintain complaint and service request records.
- Support creating, viewing, editing, and deleting records.
- Track complaint and service request status.
- Provide authentication for application users.
- Store application data in a database.
- Provide a dashboard for monitoring activities.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| HTML5 | Web page structure |
| CSS3 | User interface styling |
| JavaScript | Client-side interactions |
| XAMPP | Local server environment |
| MySQL | Database management, if configured |
| phpMyAdmin | MySQL database administration |
| GitHub | Source code hosting |

## 4. Main Features

### User Authentication
- Customer login
- Staff login
- Role-based access, according to the implemented permissions
- Validation of login credentials

### Complaint Management
- Add new complaints
- View complaint details
- Edit complaint information
- Delete complaint records
- Track complaint status and priority

### Service Request Management
- Create service requests
- View request details
- Edit service request information
- Delete service request records
- Manage request priorities and status, where implemented

### Dashboard
- Display complaint and service request summaries
- Show relevant application statistics
- Provide navigation to the main application modules

### Database Management
- Store user and application records
- Retrieve and update complaint information
- Manage service request records

## 5. Project Structure

The following is an example structure. Adjust it to match the actual folders and files in your project.

```text
complaints_service_management/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── complaint.py
│   ├── service_request.py
│   └── category.py
│
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── dashboard.py
│   ├── complaints.py
│   └── service_requests.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   └── dashboard.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│
└── database/
    └── app.db
```

**Note:** Your project may use `model` instead of `models`, and its routes or templates may have different filenames. Keep the structure consistent with the actual repository.

## 6. Requirements

- Python 3.12 or another compatible Python version
- pip package manager
- Flask and the dependencies listed in `requirements.txt`
- XAMPP, if using its MySQL database
- A modern web browser
- phpMyAdmin for managing the MySQL database

## 7. Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/amohalakshmi-04/energizenow-complaint-management.git
```

### Step 2: Open the Project Directory

```bash
cd energizenow-complaint-management
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

For Windows:

```bat
venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

## 8. XAMPP and MySQL Configuration

XAMPP provides the local server environment and MySQL database service.

### Starting XAMPP

1. Open the XAMPP Control Panel.
2. Start Apache.
3. Start MySQL.
4. Open phpMyAdmin in your browser:

   `http://localhost/phpmyadmin`

5. Select the database used by the application.
6. Verify that the required tables and records exist.

### Database Connection

Configure the Flask application with the appropriate MySQL connection settings if MySQL is the selected database.

The connection configuration may require:

- Database host
- Database port
- Database name
- Database username
- Database password

Keep actual database credentials in environment variables or a local `.env` file. Do not upload secrets to a public repository.

**Important:** Starting Apache and MySQL does not automatically connect Flask to MySQL. Verify that the application successfully connects to the intended database before describing the integration as complete.

If the application is configured to use `database/app.db`, it is using SQLite rather than XAMPP MySQL.

## 9. Customer and Staff Login

The application supports customer and staff login according to the configured user accounts and authentication logic.

### Customer Login

- Use the email address registered for the customer account.
- Enter the password assigned to that account.
- Submit the login form to access the available customer features.

### Staff Login

- Use the email address registered for the staff account.
- Enter the password assigned to that account.
- Submit the login form to access the available staff features.

### Demo Account Information

Fill in the following details only if you have verified the corresponding accounts.

| Role | Email | Password |
|---|---|---|
| Customer | Add verified demo email | Share privately with evaluator |
| Staff | Add verified demo email | Share privately with evaluator |
| Administrator | Add verified demo email, if configured | Share privately with evaluator |

**Security:** Do not publish real passwords, private customer information, or MySQL credentials in a public GitHub repository. Use dedicated demo accounts for project demonstrations. Store passwords securely as hashes rather than plain text.

## 10. Running the Application

1. Open the project directory in Command Prompt.
2. Activate the virtual environment.
3. Ensure the configured database is available and initialized.
4. Start the Flask application:

```bash
python app.py
```

5. Open the application in your browser:

`http://127.0.0.1:5000`

6. Log in using a valid customer or staff account.

## 11. Database Information

The database stores application data according to the models and database configuration implemented in the project.

Possible entities include:

- Users
- Complaints
- Service requests
- Categories

The exact tables and fields depend on the current implementation.

## 12. Validation and Error Handling

The application should validate user input and handle invalid login credentials and missing or incorrect form values appropriately.

Database errors and application exceptions should be handled safely without exposing passwords, secret keys, or sensitive internal details to users.

## 13. Future Enhancements

- Email notifications for complaint updates
- Advanced search and filtering
- Reports and analytics
- Complaint assignment to staff
- Service request progress tracking
- Improved role-based permissions
- Deployment to a production hosting platform

## 14. Author

**Project:** EnergizeNow – Complaints & Service Management System

**Backend:** Python Flask

**Purpose:** Educational project and demonstration of complaint and service request management.

## 15. License

This project is intended for educational and demonstration purposes unless a separate license is specified.


