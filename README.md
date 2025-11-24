# Set Invoice

A comprehensive, production-ready Set Invoice built with Django that allows businesses to manage customers, items, invoices, and payments efficiently. The system features a custom admin interface, role-based access control, and a modern, responsive UI built with TailwindCSS.

## 📚 Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)** - Complete setup and usage guide for end users
- **[SECURITY.md](SECURITY.md)** - Security best practices and deployment checklist
- **[ADMIN_SETUP.md](ADMIN_SETUP.md)** - Admin configuration guide

## Project Overview

This system provides a complete solution for invoice management with:
- Secure authentication and authorization
- Customer relationship management
- Inventory tracking with low stock alerts
- Professional invoice generation with PDF export
- Payment tracking and reconciliation
- Comprehensive dashboard with business metrics

## Features

### Authentication & Security
- Custom user model with email-based authentication
- Role-Based Access Control (RBAC): Admin, Manager, Staff, Viewer
- Secure password hashing (Django's PBKDF2)
- Session management with CSRF protection
- Password reset functionality
- Security headers (X-Frame-Options, XSS protection)

### Dashboard
- Overview of total invoices, pending payments, customers
- Revenue statistics (total and monthly)
- Recent activities and low stock alerts
- Quick action buttons for common tasks

### Customer Management
- Add, edit, delete, and list customers
- Search and filter customers
- View customer invoice history
- Customer status management (active/inactive)

### Inventory Management
- Manage item categories
- Add, edit, delete items
- Track total quantity and available quantity
- Low stock alerts (threshold: 10 units)
- Automatic quantity reduction when invoices are finalized
- Search and filter items

### Invoice Management
- Create new invoices with multiple items
- Auto-generate invoice numbers (format: INV-2025-0001)
- Add items dynamically with JavaScript
- Auto-calculate subtotal, tax, discount, and total
- Save as draft or finalize
- Edit draft invoices only
- Mark as paid/cancelled
- Generate PDF invoices
- Invoice status tracking (draft, pending, paid, cancelled)
- Validation: due date must be after issue date

### Payment Management
- Record payments against invoices
- Multiple payment methods (cash, card, bank transfer, online)
- Partial payment support
- Payment history per invoice
- Transaction ID tracking
- Automatic invoice status update on payment

### User Management (Admin Only)
- List all users
- Create/edit/delete users
- Assign roles to users
- Activate/deactivate users

## Technology Stack

- **Backend**: Django 5.2.8
- **Python**: 3.10+
- **Database**: SQLite (Development), PostgreSQL ready (Production)
- **Frontend**: Jinja2 Templates, TailwindCSS
- **PDF Generation**: xhtml2pdf
- **Package Management**: pip, npm

## Installation Guide

> **📖 For detailed setup instructions, see [USER_GUIDE.md](USER_GUIDE.md)**

### Prerequisites

- Python 3.10 or higher
- Node.js (for TailwindCSS)
- pip and virtualenv

### Quick Start

```bash
# Clone repository
git clone <repository-url>
cd invoice_management_system

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install TailwindCSS

```bash
npm install -D tailwindcss
npx tailwindcss init
```

### Step 5: Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your settings
```

Required environment variables:
- `SECRET_KEY`: Django secret key (generate a secure random string)
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_NAME`: Database file name (default: db.sqlite3)
- Email settings (for password reset functionality)

### Step 6: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create Superuser

```bash
python manage.py createsuperuser
```

> **⚠️ Security Note:** Never use default credentials in production. See [SECURITY.md](SECURITY.md) for best practices.

### Step 8: Build TailwindCSS

```bash
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
```

For production, build once:
```bash
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify
```

### Step 9: Run Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## Usage Guide

### Getting Started

1. **Login**: Use your credentials to access the system
2. **Setup Roles**: As admin, create user roles (Admin, Manager, Staff, Viewer)
3. **Add Categories**: Navigate to Inventory → Categories to create item categories
4. **Add Items**: Go to Inventory → Items to add products with quantities
5. **Add Customers**: Navigate to Customers → Add Customer
6. **Create Invoice**: 
   - Go to Invoices → Create Invoice
   - Select customer and add items
   - System auto-calculates totals
   - Save as draft or finalize
7. **Record Payment**: 
   - Go to Payments → Record Payment
   - Select invoice and enter payment details
   - Invoice status updates automatically

### Key Workflows

**Creating an Invoice:**
1. Select a customer
2. Add items with quantities (validated against available stock)
3. System calculates subtotal, tax, and total
4. Add discount if applicable
5. Save as draft (editable) or finalize (reduces inventory)

**Recording Payment:**
1. Select the invoice
2. Enter payment amount (supports partial payments)
3. Choose payment method
4. Add transaction ID (optional)
5. Invoice status updates to "paid" if fully paid

**Managing Inventory:**
- Available quantity is automatically reduced when invoice is finalized
- Low stock alerts appear on dashboard when available_qty < 10
- Edit items to update quantities

## Project Structure

```
invoice_management_system/
├── manage.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── config/
│   ├── settings.py          # Django settings
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── accounts/            # User authentication and management
│   ├── customers/           # Customer management
│   ├── inventory/           # Item and category management
│   ├── invoices/            # Invoice processing and PDF generation
│   ├── payments/           # Payment tracking
│   └── core/               # Dashboard and common views
├── templates/              # Jinja2 templates
│   ├── base.html
│   ├── accounts/
│   ├── customers/
│   ├── inventory/
│   ├── invoices/
│   ├── payments/
│   └── core/
├── static/
│   ├── css/               # TailwindCSS compiled files
│   ├── js/                # JavaScript files
│   └── images/            # Static images
└── media/                 # User-uploaded files (PDFs, etc.)
```

## Configuration

### Environment Variables

See `.env.example` for all available configuration options.

### Switching to PostgreSQL

1. Install PostgreSQL and psycopg2:
   ```bash
   pip install psycopg2-binary
   ```

2. Update `config/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_databaes_name',
           'USER': 'your_database_username',
           'PASSWORD': 'your_database_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

### Email Configuration

For password reset and email notifications, configure email settings in `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=johndoe@gmail.com
EMAIL_HOST_PASSWORD=johndoe_password
```

## Security Features

- **Password Security**: Django's PBKDF2 hashing algorithm
- **CSRF Protection**: Enabled on all forms
- **XSS Protection**: All user inputs are escaped in templates
- **SQL Injection Prevention**: Django ORM used throughout
- **Security Headers**: X-Frame-Options, X-Content-Type-Options
- **Session Security**: Secure session cookies in production
- **Access Control**: Role-based permissions on all views

## Database Schema

The system uses the following main tables:
- `user_roles`: User role definitions
- `users`: User accounts with role assignment
- `customer`: Customer information
- `item_category`: Item categories
- `item`: Inventory items with quantity tracking
- `invoice`: Invoice headers
- `invoice_item`: Invoice line items
- `payment`: Payment records

All tables include proper indexes for optimal query performance.

## Testing

### Running Tests

```bash
python manage.py test
```

### Test Coverage

To measure test coverage:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## Deployment Guide

### Production Checklist

1. **Environment Variables**:
   - Set `DEBUG=False`
   - Set `SECRET_KEY` to a secure random string
   - Configure `ALLOWED_HOSTS`

2. **Static Files**:
   ```bash
   python manage.py collectstatic
   ```

3. **Database**:
   - Migrate to PostgreSQL (recommended)
   - Run migrations: `python manage.py migrate`

4. **Security**:
   - Enable HTTPS
   - Configure security headers (already in settings.py)
   - Set up proper email backend

5. **Performance**:
   - Use a production WSGI server (Gunicorn, uWSGI)
   - Set up reverse proxy (Nginx)
   - Enable database connection pooling
   - Configure caching (Redis/Memcached)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to classes and functions
- Write tests for new features

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or contributions, please open an issue on the repository.

## Author

Set Invoice - Built with Django and TailwindCSS
