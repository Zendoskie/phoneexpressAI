# PhoneXpress - AI-Powered Online Phone Shop

PhoneXpress is a Django-based web application featuring an AI chatbot assistant that helps customers browse and order phones online. All prices are displayed in Philippine Peso (PHP).

## Features

- 🤖 **AI-Powered Chatbot**: Interactive chatbot using OpenRouter API to assist customers
- 📱 **Phone Catalog**: Browse available phones with detailed information
- 💰 **PHP Pricing**: All prices displayed in Philippine Peso
- 🛒 **Online Ordering**: Place orders directly through the chatbot
- 📊 **Admin Panel**: Manage phones and orders via Django admin

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd Chatbot_1
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Load initial phone data**:
   ```bash
   python manage.py load_phones
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - Home page: http://127.0.0.1:8000/
   - Chatbot: http://127.0.0.1:8000/chatbot/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
Chatbot_1/
├── manage.py                 # Django management script
├── phonexpress/             # Main project directory
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── chatbot/                 # Main app directory
│   ├── models.py            # Phone and Order models
│   ├── views.py             # Views and API endpoints
│   ├── admin.py             # Admin configuration
│   ├── management/
│   │   └── commands/
│   │       └── load_phones.py  # Command to load phone data
│   └── templates/
│       └── chatbot/
│           ├── index.html       # Intro page
│           └── chatbot.html     # Chatbot interface
├── static/
│   └── css/
│       └── styles.css       # Styling
├── requirements.txt
└── README.md
```

## API Endpoints

- `GET /` - Home/intro page
- `GET /chatbot/` - Chatbot interface
- `POST /api/chat/` - Send message to chatbot (returns AI response)
- `GET /api/phones/` - Get list of available phones
- `POST /api/order/` - Create a new order

## Usage

1. Start at the home page to learn about PhoneXpress
2. Click "Start Shopping →" to access the chatbot
3. Chat with the AI assistant to:
   - Browse available phones
   - Get pricing information
   - Ask questions about phones
   - Place orders

## Configuration

The OpenRouter API key is configured in `phonexpress/settings.py`. The API key is already set up, but you can change it if needed.

## Technologies Used

- **Django**: Web framework
- **OpenRouter API**: AI chatbot responses
- **HTML/CSS/JavaScript**: Frontend
- **SQLite**: Database (default Django database)

## Notes

- All prices are in Philippine Peso (PHP)
- The chatbot uses OpenRouter API for AI responses
- Orders are stored in the database and can be managed via admin panel

