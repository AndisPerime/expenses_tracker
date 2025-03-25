# Expenses Tracker

Expenses Tracker is a comprehensive Django-based web application designed to help users efficiently manage and track their personal or business expenses.

## Overview

This application provides a simple yet powerful interface for expense management, enabling users to track spending patterns, categorize expenses, and gain insights into their financial habits.

The live project can be viewed [here](https://expenses-tracker-app1991-ca4d3c49a2b4.herokuapp.com/)


![Expenses Tracker](https://github.com/user-attachments/assets/241e8923-8d99-4cfe-8b27-231be6a75dea)


## User Experience (UX)

The User Stories in this project are documented in GitHub Projects. 
The project board link, can find [here](https://github.com/users/AndisPerime/projects/4)

1. **User Registration, Sign in and Sign out**
2. **Export Data**
3. **Dashboard Overiew**
4. **View Transaction History**
5. **Add/Edit/Delete Income and Expense**
6. **Notifications and Alerts**
7. **Set Budget Limit**
8. **Categorize Transaction**
9. **Data Security**


## Features

- **User Authentication**
  - Secure registration and login system
  - Password reset functionality
  - User profile management
  
- **Expense Management**
  - Add, edit, view, and delete expense records
  - Bulk operations for multiple expenses
  - Search and filter capabilities
  
- **Categorization**
  - Predefined expense categories
  - Custom category creation
  - Category-based reporting
  
- **Visualization**
  - Visual representation of spending patterns
  - Monthly and yearly expense summaries
  - Category distribution charts
  
- **Additional Features**
  - Export expenses to CSV
  - Responsive design for mobile and desktop
  - Dark/light mode theme (currently not implemented)
 
## Wireframes
<details open>
<summary>Wireframe - Welcome </summary>  
   
![Welcome](https://github.com/user-attachments/assets/49c0e68f-0601-4538-bf56-d8049c56330d)


</details> 

<details>
<summary>Wireframe - Sign Up </summary>  

![sign up](https://github.com/user-attachments/assets/be86ca77-0c9b-4b49-b52e-a9e2dbfaffae)


</details> 

<details>
<summary>Wireframe - Sing in </summary>  

![sign in](https://github.com/user-attachments/assets/dc8d2a26-0164-4049-a896-5be33d800cc5)


</details> 

<details>
<summary>Wireframe - Financial Dashboard </summary>  

![financial dashboard](https://github.com/user-attachments/assets/350487d8-ef47-44f3-91c3-5eeca602a312)


</details> 

<details>
<summary>Wireframe - Budget Dashboard </summary>  

![budget dashboard](https://github.com/user-attachments/assets/456be24e-2658-4ae2-9d03-f95caa9d74fd)


</details> 


## Technologies Used

- Django (Backend framework)
- SQLite/PostgreSQL (Database)
- HTML, CSS, JavaScript (Frontend)
- Bootstrap (UI components)
- Chart.js (Data visualization)
- Balsamiq (Create wireframes)
- GitHub (Save and store all files) 
- Git (Version control)
- Visual Studio Code
- Bootstrap v5.3
- Dev Tools (Debug and for testing responsiveness)
- Google Lighthouse (Auditing the website)
- W3C Validator (Validating the HTML and CSS code)
- Heroku (Deployment)
- Wave (Web accessibility tool)

## Acknowledgments
- Django and its community for the excellent framework
- Bootstrap for the responsive design components
- TinyMCE for the rich text editing capabilities
- All open-source contributors whose libraries made this project possible

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

4. Set up environment variables (create a .env file in the root directory):
    ```
    SECRET_KEY=your_secret_key
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
    ```

5. Set up the database:
    ```sh
    python manage.py migrate
    ```

6. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

7. Run the development server:
    ```sh
    python manage.py runserver
    ```

8. Open your browser and go to `http://127.0.0.1:8000/`

## Usage

1. **Register/Login**: Create an account or log in with your credentials
2. **Dashboard**: View a summary of your expenses and spending patterns
3. **Add Expense**: Click on "Add Expense" button and fill in the expense details
4. **Categories**: Manage your expense categories from the settings section
5. **Reports**: Generate and export expense reports for selected time periods

## Deployment

The application can be deployed to various platforms:

### Heroku Deployment
1. Create a Procfile in the root directory:
   ```
   web: gunicorn expenses_tracker.wsgi
   ```
2. Add the necessary packages:
   ```sh
   pip install gunicorn dj-database-url psycopg2-binary whitenoise
   ```
3. Update settings.py for production
4. Deploy to Heroku using their CLI or GitHub integration

### VPS/Dedicated Server
1. Set up a production-ready web server (Nginx, Apache)
2. Configure WSGI with Gunicorn
3. Set up PostgreSQL
4. Use Systemd for process management


## Testing
  ### Testing browsers
  - Opera GX
  - Mozzila Firefox
  - Brave

#### **HTML Validation using W3C Validation**



#### **CSS Validation using W3C Validation**




#### **Lighthouse scores via Chrome Developer Tools**



## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Contact

Project Link: [https://github.com/AndisPerime/expenses_tracker](https://github.com/AndisPerime/expenses_tracker)
