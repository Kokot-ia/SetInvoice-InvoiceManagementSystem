# Set Invoice - User Guide

Welcome to **Set Invoice**, a comprehensive Django-based invoice management system. This guide will help you set up, configure, and use the platform effectively.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Initial Setup](#initial-setup)
4. [User Roles & Permissions](#user-roles--permissions)
5. [Core Features](#core-features)
6. [Common Workflows](#common-workflows)
7. [Troubleshooting](#troubleshooting)
8. [Security Best Practices](#security-best-practices)

---

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Node.js (for TailwindCSS)
- pip and virtualenv
- Git (optional)

### 5-Minute Setup

```bash
# 1. Clone or download the project
git clone https://github.com/Systemsetco/SetInvoice-InvoiceManagementSystem.git
cd invoice_management_system

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
npm install -D tailwindcss

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings (see Configuration section)

# 5. Setup database
python manage.py migrate

# 6. Create admin user
python manage.py createsuperuser

# 7. Build TailwindCSS (in a separate terminal)
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch

# 8. Run the server
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

---

## Installation

### Step 1: Environment Setup

Create and activate a virtual environment:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- Django 5.2.8
- django-jinja
- python-dotenv
- xhtml2pdf (for PDF generation)
- argon2-cffi (optional, for enhanced password security)

### Step 3: Install Frontend Dependencies

```bash
npm install -D tailwindcss
```

### Step 4: Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Security Settings
SECRET_KEY=your-unique-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration (for password reset and notifications)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# For production with Gmail:
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
# DEFAULT_FROM_EMAIL=Set Invoice <your-email@gmail.com>
```

> **⚠️ Important:** Never commit your `.env` file to version control!

### Step 5: Database Setup

Run migrations to create database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Initial Setup

### Creating Your First Admin User

**Option 1: Using Django's built-in command (Recommended)**

```bash
python manage.py createsuperuser
```

Follow the prompts to enter:
- Email address
- Password (minimum 8 characters)

**Option 2: Using the template script**

1. Copy the template:
   ```bash
   cp create_admin_template.py create_admin_user.py
   ```

2. Edit `create_admin_user.py` and update:
   ```python
   admin_email = 'your-email@example.com'  # Your email
   admin_password = 'YourSecurePassword123!'  # Your password
   ```

3. Run the script:
   ```bash
   python manage.py shell < create_admin_user.py
   ```

### Setting Up Test Data (Optional)

To quickly populate the system with sample data for testing:

```bash
python manage.py shell < setup_test_data.py
```

This creates:
- User roles (Admin, Manager, User)
- Sample customers
- Item categories (Electronics, Furniture, Office Supplies)
- Sample inventory items

### Building TailwindCSS

**For development (with auto-rebuild):**

```bash
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
```

Keep this running in a separate terminal while developing.

**For production (one-time build):**

```bash
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify
```

### Starting the Server

```bash
python manage.py runserver
```

Access the application at: **http://127.0.0.1:8000**

---

## User Roles & Permissions

The system supports role-based access control (RBAC):

| Role | Permissions |
|------|-------------|
| **Admin** | Full system access, user management, all CRUD operations |
| **Manager** | Create/edit invoices, customers, items, view reports |
| **User** | Create invoices, view own data, limited editing |
| **Viewer** | Read-only access to invoices and reports |

### Creating Additional Users

1. Login as Admin
2. Navigate to **Users** → **Add User**
3. Fill in user details:
   - Email address
   - Password
   - Assign role
   - Set status (Active/Inactive)
4. Click **Save**

---

## Core Features

### 1. Dashboard

The dashboard provides an overview of your business:

- **Total Invoices**: Count of all invoices
- **Pending Payments**: Invoices awaiting payment
- **Total Customers**: Active customer count
- **Revenue Statistics**: Total and monthly revenue
- **Recent Activities**: Latest invoices and payments
- **Low Stock Alerts**: Items with quantity < 10

### 2. Customer Management

**Adding a Customer:**

1. Navigate to **Customers** → **Add Customer**
2. Fill in required fields:
   - Customer Name
   - Email
   - Contact Number
   - Address
   - City
3. Click **Save**

**Managing Customers:**

- **Search**: Use the search bar to find customers by name or email
- **Edit**: Click the edit icon to modify customer details
- **Delete**: Remove customers (only if no invoices exist)
- **View History**: See all invoices for a specific customer

### 3. Inventory Management

**Creating Categories:**

1. Go to **Inventory** → **Categories**
2. Click **Add Category**
3. Enter category name (e.g., "Electronics", "Furniture")
4. Save

**Adding Items:**

1. Navigate to **Inventory** → **Items**
2. Click **Add Item**
3. Fill in details:
   - Item Name
   - Category
   - Price
   - Available Quantity
   - Description (optional)
4. Save

**Stock Management:**

- Items with **available quantity < 10** trigger low stock alerts
- Quantity automatically reduces when invoices are finalized
- Edit items to update stock levels

### 4. Invoice Management

**Creating an Invoice:**

1. Go to **Invoices** → **Create Invoice**
2. Select customer from dropdown
3. Set issue date and due date
4. Add items:
   - Click **Add Item**
   - Select item from dropdown
   - Enter quantity (validated against available stock)
   - Price auto-fills, can be adjusted
   - Subtotal calculates automatically
5. Apply discount (optional)
6. Tax is calculated automatically (configurable)
7. Choose action:
   - **Save as Draft**: Invoice can be edited later
   - **Finalize**: Invoice is locked, inventory reduced

**Invoice Statuses:**

- **Draft**: Editable, no inventory impact
- **Pending**: Finalized, awaiting payment
- **Paid**: Payment received
- **Cancelled**: Invoice voided

**Editing Invoices:**

- Only **Draft** invoices can be edited
- Navigate to **Invoices** → Click edit icon
- Make changes and save

**Generating PDF:**

1. Open invoice details
2. Click **Download PDF**
3. Professional PDF invoice is generated

### 5. Payment Management

**Recording a Payment:**

1. Go to **Payments** → **Record Payment**
2. Select invoice from dropdown
3. Enter payment details:
   - Amount (supports partial payments)
   - Payment method (Cash, Card, Bank Transfer, Online)
   - Transaction ID (optional)
   - Payment date
4. Click **Save**

**Payment Tracking:**

- View all payments for an invoice
- Invoice status updates automatically:
  - Fully paid → Status: **Paid**
  - Partially paid → Status: **Pending**
- Payment history maintained for auditing

---

## Common Workflows

### Workflow 1: Complete Invoice Process

```
1. Add Customer (if new)
   ↓
2. Add Items to Inventory
   ↓
3. Create Invoice
   - Select customer
   - Add items with quantities
   - Apply discount if needed
   - Finalize invoice
   ↓
4. Generate PDF Invoice
   ↓
5. Send to Customer
   ↓
6. Record Payment when received
   ↓
7. Invoice marked as Paid
```

### Workflow 2: Managing Low Stock

```
1. Check Dashboard for low stock alerts
   ↓
2. Navigate to Inventory → Items
   ↓
3. Find items with low quantity
   ↓
4. Edit item and update available quantity
   ↓
5. Alert clears from dashboard
```

### Workflow 3: Monthly Reporting

```
1. Go to Dashboard
   ↓
2. View monthly revenue statistics
   ↓
3. Navigate to Invoices
   ↓
4. Filter by date range
   ↓
5. Export or review invoice list
   ↓
6. Check Payments for reconciliation
```

---

## Troubleshooting

### Issue: Cannot Login

**Solution:**
- Verify email and password are correct
- Check if user account is active (Admin can verify)
- Ensure email verification is complete (if enabled)
- Try password reset functionality

### Issue: TailwindCSS Styles Not Loading

**Solution:**
```bash
# Rebuild TailwindCSS
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css

# Clear browser cache
# Restart Django server
python manage.py runserver
```

### Issue: Email Not Sending

**Solution:**
1. Check `.env` file for correct email configuration
2. For Gmail, enable "App Passwords":
   - Go to Google Account → Security
   - Enable 2-Factor Authentication
   - Generate App Password
   - Use App Password in `.env`
3. Test email configuration:
   ```bash
   python check_env.py
   ```

### Issue: Database Errors

**Solution:**
```bash
# Reset database (WARNING: Deletes all data)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue: "Item out of stock" Error

**Solution:**
- Check available quantity in Inventory → Items
- Update stock levels before creating invoice
- Reduce quantity in invoice to match available stock

### Issue: Cannot Edit Invoice

**Solution:**
- Only **Draft** invoices can be edited
- Finalized invoices are locked for data integrity
- Create a new invoice or cancel existing one

---

## Security Best Practices

### For Development

1. **Keep `.env` secure:**
   - Never commit to version control
   - Use `.env.example` as template
   - Rotate secrets regularly

2. **Use strong passwords:**
   - Minimum 8 characters
   - Mix of uppercase, lowercase, numbers, symbols
   - Avoid common passwords

3. **Regular backups:**
   ```bash
   # Backup database
   cp db.sqlite3 backups/db_backup_$(date +%Y%m%d).sqlite3
   ```

### For Production

1. **Update `.env` settings:**
   ```env
   DEBUG=False
   SECRET_KEY=<generate-new-secure-key>
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

2. **Use PostgreSQL instead of SQLite:**
   - Install: `pip install psycopg2-binary`
   - Update `config/settings.py` database configuration

3. **Enable HTTPS:**
   - Use SSL certificate
   - Configure reverse proxy (Nginx/Apache)

4. **Collect static files:**
   ```bash
   python manage.py collectstatic
   ```

5. **Use production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn config.wsgi:application
   ```

6. **Regular updates:**
   - Keep Django and dependencies updated
   - Monitor security advisories
   - Apply patches promptly

---

## Email Configuration Guide

### Development (Console Backend)

For testing, emails print to console:

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Production (Gmail)

1. Enable 2-Factor Authentication on Google Account
2. Generate App Password:
   - Google Account → Security → App Passwords
   - Select "Mail" and your device
   - Copy generated password

3. Update `.env`:
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=Set Invoice <your-email@gmail.com>
   ```

### Production (SendGrid)

1. Create SendGrid account
2. Generate API key
3. Update `.env`:
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.sendgrid.net
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=apikey
   EMAIL_HOST_PASSWORD=your-sendgrid-api-key
   DEFAULT_FROM_EMAIL=Set Invoice <noreply@yourdomain.com>
   ```

---

## Additional Resources

### Useful Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (production)
python manage.py collectstatic

# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080

# Access from network
python manage.py runserver 0.0.0.0:8000
```

### Project Structure

```
invoice_management_system/
├── apps/
│   ├── accounts/      # User authentication
│   ├── customers/     # Customer management
│   ├── inventory/     # Items and categories
│   ├── invoices/      # Invoice processing
│   ├── payments/      # Payment tracking
│   └── core/          # Dashboard and common views
├── config/            # Django settings
├── templates/         # HTML templates
├── static/            # CSS, JS, images
├── media/             # User uploads (PDFs)
└── manage.py          # Django management script
```

### Getting Help

- **Documentation**: Check README.md for technical details
- **Issues**: Report bugs on GitHub repository
- **Email**: Contact system administrator

---

## Frequently Asked Questions

**Q: Can I use this for multiple businesses?**
A: Yes, each user can manage their own customers, items, and invoices independently.

**Q: Is there a mobile app?**
A: Currently web-based only, but responsive design works on mobile browsers.

**Q: Can I customize invoice templates?**
A: Yes, edit templates in `templates/invoices/` directory.

**Q: How do I backup my data?**
A: Copy `db.sqlite3` file regularly. For production, use PostgreSQL with automated backups.

**Q: Can I export data to Excel?**
A: Currently supports PDF export. Excel export can be added as a custom feature.

**Q: What payment methods are supported?**
A: Cash, Card, Bank Transfer, and Online payments are tracked. Actual payment processing requires integration with payment gateways.

---

## Version Information

- **Django**: 5.2.8
- **Python**: 3.10+
- **TailwindCSS**: Latest
- **Database**: SQLite (dev), PostgreSQL (production)

---

## License

MIT License - See LICENSE file for details

---

**Happy Invoicing! 🧾**

For technical support or feature requests, please contact your system administrator or open an issue on the project repository.
