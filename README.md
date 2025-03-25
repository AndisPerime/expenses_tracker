# Expenses Tracker

A comprehensive web application for tracking personal expenses and managing budgets with a clean, responsive interface and theme customization options.

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

### Core Functionality
- **Expense Tracking**: Log and categorize daily expenses
- **Budget Management**: Create and monitor budgets for different expense categories
- **Dashboard**: Visual overview of spending patterns and financial status
- **User Authentication**: Secure login and registration system

### User Interface
- **Responsive Design**: Fully functional on mobile, tablet, and desktop devices
- **Dark/Light Mode**: Toggle between themes with persistent user preference
- **Mobile Navigation**: Hamburger menu for enhanced mobile experience
- **User Notifications**: Automatic message display with timed dismissal

### Technical Features
- **Django Backend**: Robust Python-based web framework
- **User Authentication**: Built with Django allauth for secure account management
- **Responsive Frontend**: Custom CSS with mobile-first approach
- **Theme Persistence**: Local storage for saving user theme preferences
- **Accessibility**: ARIA labels and semantic HTML structure

## AI Contribution

GitHub Copilot was used in the following aspects of development:

- **Theme Toggle Functionality**: AI helped debug and enhance the dark/light mode switching system
- **User Interface Structure**: Suggested best practices for responsive navigation
- **Code Refactoring**: Improved theme.js implementation with better organization and fallback handling
- **Documentation**: Assisted in generating this comprehensive README

## Developer Contribution

The developer (AndisPerime) was responsible for:

- **Core Application Architecture**: Database design, Django models, views, and URLs
- **Business Logic**: Budget calculation algorithms and expense tracking logic
- **UI/UX Design**: Visual design, CSS implementation, and user experience flow
- **Testing & Debugging**: Manual testing across devices and browsers, resolving cross-browser issues
- **Integration**: Connecting frontend and backend components
- **Security Implementations**: User authentication flow and data protection
- **Performance Optimization**: Ensuring fast load times and smooth interactions

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
<summary>Wireframe - Sing In </summary>  

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

1. Clone the repository
```
git clone https://github.com/AndisPerime/expenses_tracker.git
cd expenses_tracker
```

2. Set up a virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Apply migrations
```
python manage.py migrate
```

5. Run the development server
```
python manage.py runserver
```

6. Access the application at http://localhost:8000

## Future Enhancements

- Expense analytics with detailed charts and reports
- Export functionality for financial data
- Multi-currency support
- Budget prediction based on spending patterns
- Mobile app version

## Testing
  ### Testing browsers
  - Opera GX
  - Mozzila Firefox
  - Brave

#### **HTML Validation using W3C Validation**

![Screenshot 2025-03-25 142406](https://github.com/user-attachments/assets/a8e61b4b-7229-4832-b586-b3f0c5e307e5)


#### **CSS Validation using W3C Validation**

![css](https://github.com/user-attachments/assets/47c84fab-01e1-4fce-b985-3c39d080feba)


#### **Lighthouse scores via Chrome Developer Tools**

![lightscore](https://github.com/user-attachments/assets/d52c07ae-90d7-4ff9-9812-76afd84ea4c9)

## Issues

**Contributor mistake.**

Projects repository shows that there has been made a contribution by different username, but  there was an issue when another person was working on the same VScode application and the project developer forgot to check if the sign-in details into VScode were changed back to his details through terminal. 
Noticed this issue only when pushed changes to GitHub and it showed up like a different contributor, but looking into contributors tab, there was never a contributor added. Project author was the one making those changes, not being aware of different 'user.name'.


<details>
<summary>Issue Evidence </summary>  
   
![1](https://github.com/user-attachments/assets/785f6ceb-3f9f-489a-83d0-e70c5eaee450)

![2](https://github.com/user-attachments/assets/a44e3a8a-27b4-4c5c-867d-79d8233b9b7a)

![3](https://github.com/user-attachments/assets/99d5dceb-f940-4468-9f14-a598faa7aebd)

![4](https://github.com/user-attachments/assets/04749c3b-699f-45e4-8ed2-6650838c3689)

</details> 


**App issues**

1. Page for printing budget report does not have a dark mode.
2. On budget dashboard page, option to change months does not work, only current month is available to view.
3. Sign-up and login both have 2 different working versions of pages.


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

---

© 2023 Expenses Tracker by AndisPerime. All rights reserved.
