from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    """
    Admin configuration for Contact Model.
    """

    list_display = ('name', 'email', 'subject', 'created_on')
    search_fields = ('name', 'email', 'subject', 'body')


admin.site.register(Contact, ContactAdmin)
