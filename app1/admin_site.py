from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = "BJP Kottayam-West"
    site_title = "BJP Kottayam-West Admin Portal"
    index_title = "Welcome to BJP Kottayam-West Admin"

admin_site = CustomAdminSite(name='custom_admin')
