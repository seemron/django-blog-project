from django.contrib import admin
from .models import BlogPost  # ✅ No AccessRequest or ApprovedUser

admin.site.register(BlogPost)
# admin.site.register(PrivatePostAccess)
from .models import AccessRequest

@admin.register(AccessRequest)
class AccessRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('user__username',)
    actions = ['approve_requests']

    def approve_requests(self, request, queryset):
        queryset.update(is_approved=True)
    approve_requests.short_description = "Approve selected requests"

from .models import ApprovedEmail

@admin.register(ApprovedEmail)
class ApprovedEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'approved')
    list_filter = ('approved',)
    search_fields = ('email',)