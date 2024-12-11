# Personal Finance Tracker

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: 
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up the PostgreSQL database
6. Create a `.env` file with the necessary environment variables
7. Run migrations: `python manage.py migrate`
8. Start the Django development server: `python manage.py runserver`
9. In a new terminal, navigate to the `frontend` directory
10. Install frontend dependencies: `npm install`
11. Start the React development server: `npm start`

The application should now be running at `http://localhost:3000`