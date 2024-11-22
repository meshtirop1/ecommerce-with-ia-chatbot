# ecommerce-with-ia-chatbot
Django E-commerce Platform with Flask Chatbot Integration
📖 Overview
This project combines a Django-based e-commerce platform with a Flask-based chatbot to deliver a robust and interactive shopping experience. The chatbot enhances customer interaction by providing real-time assistance with product inquiries, order tracking, and payment details. The platform also supports secure payment integration and responsive design for seamless usability.

🚀 Features
E-commerce Platform
User authentication (login, register, logout).
Product browsing and detailed view.
Search functionality for products.
Responsive design for mobile and desktop.
Integration with PayPal for secure payments.
Flask Chatbot
Flask application embedded into the Django platform.
Provides real-time assistance for:
Product price inquiries.
Shipment tracking.
Payment assistance.
Accesses data dynamically from the Django SQLite3 database.
Redirects complex queries to human support.
Operates only for authenticated users.
Built with NLTK for natural language processing.
🛠️ Technologies Used
Backend
Django (Python) for the e-commerce platform.
Flask (Python) for the chatbot.
SQLite3 for database management.
Frontend
HTML, CSS
JavaScript for interactivity
Bootstrap for responsive design
Chatbot
NLTK for intent detection and response generation.
Flask API for chatbot interactions.
📂 Project Structure
plaintext
Copy code
django_chatbot/
│
├── ecommerce/               # Django project
│   ├── settings.py         # Django project settings
│   ├── urls.py             # URL routing for the project
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── templates/          # HTML templates
│   └── static/             # Static files (CSS, JS, images)
│
├── chatbot/                 # Flask chatbot project
│   ├── app.py              # Flask application
│   ├── intents.json        # Chatbot intents data
│   ├── train_model.py      # Intent classification model training
│   ├── responses.py        # Chatbot response logic
│   └── templates/          # Chatbot UI templates
│
├── db.sqlite3              # Project database
├── manage.py               # Django project management script
├── requirements.txt        # Python dependencies
└── .gitignore              # Files and folders to ignore in version control
⚙️ Setup Instructions
Prerequisites
Python 3.12+
pip (Python package installer)
SQLite3 installed locally
Django and Flask installed
NLTK library installed
Installation Steps
Clone the repository:

bash
Copy code
git clone https://github.com/meshtirop1/ecommerce-ai-chatbot.git
cd django-chatbot
Create a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Apply migrations for Django:

bash
Copy code
python manage.py migrate
Start the Django server:

bash
Copy code
python manage.py runserver
Navigate to the chatbot directory and run the Flask server:

bash
Copy code
cd chatbot
python app.py
Access the project in your browser at http://127.0.0.1:8000/ for Django and the chatbot endpoint for Flask.

🛡️ Security
User authentication ensures access control.
Sensitive data such as database credentials are protected using environment variables.
PayPal integration is implemented for secure payment processing.
📦 Deployment
For production, consider:

E-commerce platform: Deploy Django using Gunicorn and Nginx.
Chatbot: Deploy Flask using Gunicorn or a similar WSGI server.
Database: Migrate to PostgreSQL for scalability.
✨ Future Enhancements
Multi-language chatbot support.
Enhanced intent detection using custom NLP models.
Integration with third-party APIs for shipping and tracking.
🤝 Contributing
Contributions are welcome! Follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature-name).
Commit your changes (git commit -m "Add feature-name").
Push to the branch (git push origin feature-name).
Open a pull request.
📝 License
This project is licensed under the MIT License. See the LICENSE file for details.

📧 Contact
For any inquiries, please reach out to:

Name: Meshack Tirop
Email:mtirop345@gmail.com
