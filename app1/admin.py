from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import User, Group
from django.contrib.admin import AdminSite
from .models import UserModel, Constituency, LocalBody, MeetingReport

# ✅ 1. Define custom AdminSite
class CustomAdminSite(AdminSite):
    site_header = "BJP Kottayam-West"
    site_title = "BJP Kottayam-West Admin Portal"
    index_title = "Welcome to BJP Kottayam-West Admin"

    class Media:
        css = {
            'all': ('css/custom_admin.css',)  # path inside static/
        }


# ✅ 2. Create instance of custom AdminSite
custom_admin_site = CustomAdminSite(name='custom_admin')

# ✅ 3. Custom Inline
class LocalBodyInline(admin.TabularInline):
    model = LocalBody
    fields = ('name', 'new_ward_count_display')  # ⬅️ changed from 'type' to 'name'
    readonly_fields = fields
    extra = 0
    can_delete = False
    show_change_link = False

    def new_ward_count_display(self, obj):
        return obj.new_ward_count

    new_ward_count_display.short_description = 'Ward Count'


# ✅ 4. Custom Constituency Admin
class ConstituencyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [LocalBodyInline]
    actions = None

# ✅ 5. Read-only MeetingReport admin
class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    def image1_tag(self, obj):
        if obj.image1:
            return format_html('<img src="{}" width="100" height="100" />', obj.image1.url)
        return "-"
    def image2_tag(self, obj):
        if obj.image2:
            return format_html('<img src="{}" width="100" height="100" />', obj.image2.url)
        return "-"

    def local_body_type(self, obj):
        return obj.local_body.type
    local_body_type.short_description = "Local Body Type"

    ordering = ['meeting_report_id']
    image1_tag.short_description = 'Image 1'
    image2_tag.short_description = 'Image 2'

    list_display = (
        'meeting_report_id', 'constituency', 'local_body', 'local_body_type', 'ward_number',
        'ward_incharge', 'mobile_number','office_bearer_name',
         'meeting_date', 'number_of_attendees',
        'image1_tag', 'image2_tag',
    )

    readonly_fields = [field.name for field in MeetingReport._meta.fields] + ['image1_tag', 'image2_tag', 'local_body_type']

class LocalBodyAdmin(admin.ModelAdmin):
        list_display = ('name', 'type', 'old_ward_count', 'new_ward_count')
        actions = None

# ✅ 6. Register your models with custom admin site
custom_admin_site.register(Constituency, ConstituencyAdmin)
custom_admin_site.register(LocalBody, LocalBodyAdmin)
custom_admin_site.register(MeetingReport, ReadOnlyAdmin)


