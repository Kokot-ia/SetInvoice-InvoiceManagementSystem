# Admin User Creation Guide

## Method 1: Using Python Script (Recommended) ✅

### Step 1: Run the script
```bash
python manage.py shell < create_admin_user.py
```

### Step 2: Login
- URL: http://127.0.0.1:8000/accounts/login/
- Email: `admin@example.com`
- Password: `admin123`

---

## Method 2: Using Django Shell (Manual)

### Step 1: Open Django shell
```bash
python manage.py shell
```

### Step 2: Run these commands
```python
from apps.accounts.models import Users, User_Roles

# Create Admin role
admin_role, created = User_Roles.objects.get_or_create(role_name='Admin')

# Create admin user
admin = Users.objects.create_user(
    email='admin@example.com',
    password='admin123',
    role=admin_role,
    status=1
)

print("Admin created!")
exit()
```

---

## Method 3: Assign Role to Existing User

Agar user already exist karta hai aur usko Admin banana hai:

```python
from apps.accounts.models import Users, User_Roles

# Get the user
user = Users.objects.get(email='existing@example.com')

# Get or create Admin role
admin_role, created = User_Roles.objects.get_or_create(role_name='Admin')

# Assign role
user.role = admin_role
user.status = 1  # Make sure user is active
user.save()

print(f"{user.email} is now an Admin!")
```

---

## Available Roles

Aap different roles bana sakte ho:

```python
from apps.accounts.models import User_Roles

# Create different roles
User_Roles.objects.get_or_create(role_name='Admin')
User_Roles.objects.get_or_create(role_name='Manager')
User_Roles.objects.get_or_create(role_name='Staff')
User_Roles.objects.get_or_create(role_name='Viewer')
```

---

## Login Credentials (Default)

📧 **Email**: `admin@example.com`  
🔑 **Password**: `admin123`  
👤 **Role**: Admin

---

## Important Notes

1. **Password Change**: Login ke baad password change kar lena
2. **Production**: Production mein strong password use karna
3. **Email**: Real email address use karna for password reset
4. **Roles**: Roles ko database mein manually bhi add kar sakte ho

---

## Troubleshooting

### Error: "User already exists"
```python
# Delete existing user
Users.objects.filter(email='admin@example.com').delete()
# Then create again
```

### Error: "Role does not exist"
```python
# Create role first
User_Roles.objects.create(role_name='Admin')
```

### Check existing users
```python
from apps.accounts.models import Users
for user in Users.objects.all():
    print(f"{user.email} - Role: {user.role.role_name if user.role else 'No Role'}")
```
