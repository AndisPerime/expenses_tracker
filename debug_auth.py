"""
Debug script to check authentication setup.
Run this with: python manage.py shell < debug_auth.py
"""

from django.conf import settings
from django.urls import reverse, resolve
import sys

print("\n=== Django AllAuth Debug Information ===\n")

# Check if allauth is in installed apps
print("AllAuth in INSTALLED_APPS:", 'allauth' in settings.INSTALLED_APPS)
print("AllAuth Account in INSTALLED_APPS:", 'allauth.account' in settings.INSTALLED_APPS)

# Check authentication backends
print("\nAuthentication Backends:")
for backend in settings.AUTHENTICATION_BACKENDS:
    print(f"- {backend}")

# Check template directories
print("\nTemplate Directories:")
for template in settings.TEMPLATES:
    for directory in template.get('DIRS', []):
        print(f"- {directory}")

# Check login URL settings
print("\nAuthentication URLs:")
print(f"LOGIN_URL: {settings.LOGIN_URL}")
print(f"LOGIN_REDIRECT_URL: {settings.LOGIN_REDIRECT_URL}")
print(f"LOGOUT_REDIRECT_URL: {settings.LOGOUT_REDIRECT_URL}")

# Check AllAuth settings
print("\nAllAuth Settings:")
print(f"ACCOUNT_EMAIL_VERIFICATION: {getattr(settings, 'ACCOUNT_EMAIL_VERIFICATION', 'N/A')}")
print(f"ACCOUNT_AUTHENTICATION_METHOD: {getattr(settings, 'ACCOUNT_AUTHENTICATION_METHOD', 'N/A')}")

# Try to resolve some URLs
print("\nURL Resolution:")
try:
    print(f"account_login resolves to: {resolve(reverse('account_login'))}")
    print(f"account_signup resolves to: {resolve(reverse('account_signup'))}")
except Exception as e:
    print(f"Error resolving URLs: {e}")

print("\n=== End of Debug Information ===\n")
sys.exit(0)
