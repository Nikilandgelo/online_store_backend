# 🌐 Project Overview
This project is an online marketplace platform, developed as part of a graduate assignment, that provides essential e-commerce functionality. The platform allows users to manage products, shops, and orders with a robust user role system (Admin, Shop Owner, Customer). It is designed with scalability and modern best practices in mind, ensuring security, easy maintenance, and future extensibility.

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Nikilandgelo/online_store_backend/CI.yml?style=for-the-badge&logo=githubactions&logoColor=white&label=CI&labelColor=blue)

## 🚀 Key Features

- 🔒 **User Authentication & Authorization**: Users can register, log in, confirm their emails via the API, and request password reset links. Different roles (Admin, Shop Owner, Customer) ensure role-based access control throughout the platform.

- 🗂 **Category Management**: Admins can create, update, and delete categories, and also manage shops within categories.

- 🏪 **Shop & Product Management**: Authenticated users can create and manage their own shops, update or delete them, and handle products through manual input (update/delete) or import from file (`JSON`, `YAML`).

- 🛒 **Shopping Cart & Order System**: Users can add, view and remove products from their shopping cart, place orders, confirm them and view order history. Admins are responsible for managing order statuses and can delete orders.

- 📧 **Asynchronous Email Notifications**: `Celery` workers, with `Redis` as the message broker, manage email notifications for users and admins.

- 🐋 **Dockerized Environment**: The platform is fully containerized using `Docker` and `Docker Compose`, simplifying local development and deployment by including the backend, `PostgreSQL` database, and `Redis` for message brokering.

- 📜 **Process Management**: Supervisor efficiently manages both `Django` and `Celery` processes within a single container, ensuring logs are handled smoothly.

- 🛠️ **CI/CD Pipeline**: `GitHub Actions` are integrated for continuous integration, ensuring code quality with automated testing, linting, and coverage reports before merging changes to the main branch.

## 💻 Technologies Used
| **Backend**                                                        | **DevOps**                                             | **Databases & Message Broker**                 |
| -----------                                                        | -----------                                            | -----------                                    |
| [`Python`](https://www.python.org/)                                | [`Docker`](https://docs.docker.com/)                   | [`PostgreSQL`](https://www.postgresql.org/)    |
| [`Django`](https://www.djangoproject.com/)                         | [`Docker Compose`](https://docs.docker.com/compose/)   | [`Redis`](https://redis.io/)                   |
| [`DjangoRestFramework`](https://www.django-rest-framework.org/)    | [`GitHub Actions`](https://docs.github.com/en/actions) |                                                |
| [`Celery`](https://docs.celeryq.dev/en/stable/index.html)          |                                                        |                                                |

## 📜 API Documentation
You can explore all the API endpoints in the Postman documentation. [Click here](https://documenter.getpostman.com/view/35303425/2sAXqmBkXG#8ba2ba64-94f0-4ce5-bc79-339a8701e6e7) to view the detailed documentation.

## ⚙️ Requirements
- [Python 3.12](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/)
- [Git](https://git-scm.com/downloads)

## 🛠️ Setup & Installation
### Steps:
  1. 📥 **Clone the repository**  
  First, ensure you have `git` installed on your machine. Then clone the project repository:
  ```bash
   
    git clone https://github.com/Nikilandgelo/online_store_backend.git
   
  ```
  2. 📝 **Create a `.env` file**  
  In the root directory of the project, create a `.env` file with the following variables (make sure to replace `<...>` with your own values):
  - For `PostgreSQL`:
  ```env

    POSTGRES_PASSWORD=<your_postgres_password>
    POSTGRES_USER=<your_postgres_user>
    POSTGRES_DB=<your_postgres_db>
    POSTGRES_HOST=PostgresDB
    POSTGRES_PORT=5432

  ```
  - For email handling (ensure you have access to a SMTP server):
  ```env

    EMAIL_HOST=<your_smtp.example.com>
    EMAIL_HOST_PASSWORD=<your_email_password>
    EMAIL_HOST_USER=<your_email_user>
    EMAIL_PORT=<587> or <465>
    SERVER_SOCKET=localhost:8000                      # your django server IP:port
    ADMIN_EMAIL=<your_another_email_user>             # for getting  "admins" mails when orders confirmed

  ```
  - Other Django settings:
  ```env

    SECRET_KEY=<your_secret_key>
    REDIS_HOST=Redis

  ```
  3. 📂 **Navigate to the project directory**:  
  Once the repository is cloned, navigate to the `DRFProject` directory where the main backend files are located:
  ```bash
     
    cd DRFProject
     
  ```
  4. 🔧 **Set up a virtual environment and install dependencies**:  
  Create a virtual environment for the project and install the required Python dependencies:
  ```bash
    python -m venv .venv/                # Create a virtual environment
    source .venv/bin/activate            # Activate the virtual environment on Linux
                                         # on Windows will be - venv\Scripts\activate
    pip install -r requirements.txt      # Install all dependencies

  ```
  5. 🐋 **Run the Docker containers**:  
  Finally, start up all required services (PostgreSQL, Redis, Django) by running the Docker containers:
  ```bash
     
    docker-compose up -d --build
     
  ```
  6. 🌐 **Access the application**:  
  After the containers are running, you can access the application in your web browser at:
  ```bash
   
    http://localhost:8000
   
  ```
