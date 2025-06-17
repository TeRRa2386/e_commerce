# Bakery at Home

This project was created as part of a Python web development course.

It simulates an online bakery shop where users can browse products, add them to a shopping cart, and fill out a checkout form.

### Important Notes

- **This is not a real store.** No products are sold through this website.
- **The payment system is purely visual** and does not connect to any real payment service or gateway.
- This was made entirely for **educational purposes** to practice Flask, session management, form handling, and database interactions using SQLAlchemy.

### Features

- Flask-based backend
- Shopping cart using Flask sessions
- Bootstrap 5 responsive layout
- Modal-based cart and checkout
- SQLite database for order storage
- Form validation with Bootstrap

---

### To run locally

1. Clone the repo
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create the database:
   ```python
   from main import app
   from models import db
   with app.app_context():
       db.create_all()
   ```
5. Run the app:
   ```bash
   flask run
   ```

Enjoy building it!
