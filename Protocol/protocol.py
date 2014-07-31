# Example of how to access the Django ORM externally

# First of all we need to add satnet-release-1/WebServices to the path
# to import Django modules
import os, sys
sys.path.append(os.path.dirname(os.getcwd())+"/WebServices")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

# Import your models for use in your script
from django.contrib.auth import User

# Start of application script (demo code below)
sample_user = UserProfile.objects.all()
print sample_user[0].username
