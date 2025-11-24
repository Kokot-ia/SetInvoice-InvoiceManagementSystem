"""
Safe Admin User Creation Script Template
Copy this file and modify with your credentials before running.

Usage:
1. Copy this file: cp create_admin_template.py create_admin_user.py
2. Edit create_admin_user.py with your email and password
3. Run: python manage.py shell < create_admin_user.py
"""

from apps.accounts.models import Users, User_Roles

print("=" * 50)
print("Creating Admin User")
print("=" * 50)

# Step 1: Create or get Admin role
admin_role, created = User_Roles.objects.get_or_create(
    role_name='Admin',
    defaults={'role_name': 'Admin'}
)

if created:
    print("✅ Admin role created")
else:
    print("ℹ️  Admin role already exists")

# Step 2: Configure your admin credentials here
# IMPORTANT: Change these values before running!
admin_email = 'your-email@example.com'  # ⚠️ CHANGE THIS
admin_password = 'YourSecurePassword123!'  # ⚠️ CHANGE THIS

# Validate credentials
if admin_email == 'your-email@example.com' or admin_password == 'YourSecurePassword123!':
    print("\n❌ ERROR: Please update admin_email and admin_password in this script!")
    print("   Edit this file and change the default values before running.")
    exit(1)

# Step 3: Check if admin user already exists
if Users.objects.filter(email=admin_email).exists():
    print(f"⚠️  User with email {admin_email} already exists")
    user = Users.objects.get(email=admin_email)
    
    # Update role if needed
    if user.role != admin_role:
        user.role = admin_role
        user.status = 1  # Active
        user.email_verified = True  # Mark as verified
        user.save()
        print(f"✅ Updated user role to Admin")
    else:
        print(f"ℹ️  User already has Admin role")
        # Make sure user is active and verified
        user.status = 1
        user.email_verified = True
        user.save()
        print(f"✅ User status updated")
else:
    # Step 4: Create admin user
    admin_user = Users.objects.create_user(
        email=admin_email,
        password=admin_password,
        role=admin_role,
        status=1,  # Active
        email_verified=True  # Skip email verification for admin
    )
    print("✅ Admin user created successfully!")

print("\n" + "=" * 50)
print("Login Credentials:")
print("=" * 50)
print(f"📧 Email:    {admin_email}")
print(f"🔑 Password: {'*' * len(admin_password)}")
print(f"👤 Role:     {admin_role.role_name}")
print("=" * 50)
print("\n✅ You can now login at: http://127.0.0.1:8000/accounts/login/")
