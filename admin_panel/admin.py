# In admin_panel/admin.py

from django.contrib import admin

# Remove the import of AdminDattaSettings and the custom admin site

# If you have any models to register, do it like this:
# from .models import YourModel
# admin.site.register(YourModel)

# You can customize the admin site here if needed
admin.site.site_header = "RAEREX Administration"
admin.site.site_title = "RAEREX Admin Portal"
admin.site.index_title = "Welcome to RAEREX Admin Portal"