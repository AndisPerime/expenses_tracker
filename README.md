# Expenses Tracker

Expenses Tracker is a Django-based web application that allows users to track their expenses.

## Features

- User authentication (login and registration)
- Add, view, and manage expenses
- Categorize expenses
- Responsive design

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/AndisPerime/expenses_tracker.git
    cd expenses_tracker
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```sh
    python manage.py migrate
    ```

5. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```sh
    python manage.py runserver
    ```

7. Open your browser and go to `http://127.0.0.1:8000/`

## Deployment

To deploy the application, you can use platforms like Heroku. Make sure to set the necessary environment variables and update the `ALLOWED_HOSTS` in `settings.py`.

## License

This project is licensed under the MIT License.