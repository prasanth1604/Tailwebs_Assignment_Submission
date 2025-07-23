# Building a Robust Teacher Portal with Python, HTML & JavaScript

## 📘 Project Overview

This is a secure web application designed to authenticate faculty members within an educational institution and grant them access to a personalized dashboard. This system ensures that only authorized faculty can access sensitive academic or administrative resources.

## ✅ Features

- 🔐 **Faculty Authentication**: Secure login using Faculty ID and password.
- 📋 **Credential Verification**: Matches login credentials against a database of faculty records.
- 🔄 **Session Management**: Maintains user sessions to ensure continuous authenticated access.
- 🧭 **Dashboard Redirection**: Authenticated users are redirected to a protected dashboard.
- 💬 **User Feedback**: Provides real-time success and error messages on login.

---

## 🛠️ Technologies Used

- **Django**: High-level Python web framework for rapid development.
- **Django ORM**: Abstracts raw SQL into Python-based data operations.
- **Session-Based Authentication**: Server-side session tracking.
- **Django Messages Framework**: For user-friendly alerts and notifications.
- **Django Templating Engine**: For rendering dynamic HTML content.

---

## ⚙️ Setup and Installation

###  Clone the Repository

- Please consider creating a virtual environment

#### Requirements
To install requirements type

```
pip install -r requirements.txt
```

```
git clone https://github.com/prasanth1604/Tailwebs_Assignment_Submission.git
cd Tailwebs_Assignment_Submission
```

To migrate the database open terminal in project directory and type

```
python manage.py makemigrations
python manage.py migrate
```

## To run the program in local server use the following command

```
python manage.py runserver
```

## Initial Data Setup (Creating Faculty Members):

- After setting up the database and creating a superuser, you can create faculty records.

- Via Django Admin:

- Create a faculty model - username(used in login page), faculty name and password 


## Run the development server: python manage.py runserver

- Access the Django admin panel, usually at 
```
http://127.0.0.1:8000/admin/
```
- Log in with the superuser credentials you created.

- Navigate to the "Faculty" section and click "Add Faculty" to create new faculty members, providing their fId and password (remember to use hashed passwords if you implement that improvement).


## 🚀 Usage

- Go to /login/

- Enter valid Faculty ID and password.

- On successful login, you'll be redirected to your faculty dashboard.
