from django.contrib import admin

from .forms import AccountAdminForm
from .models import Account, HistoricalPurchase


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Account._meta.get_fields()]
    list_display_links = ["uuid"]
    list_filter = ("deleted", "is_active")
    form = AccountAdminForm
    actions = ["enable", "disable", "restore", "logical_erase"]
    search_fields = ["email", "username", "first_name", "last_name"]

    def enable(self, request, queryset):
        for ad in queryset:
            ad.enable()

    def disable(self, request, queryset):
        for ad in queryset:
            ad.disable()

    def logical_erase(self, request, queryset):
        for ad in queryset:
            ad.logical_erase()

    def restore(self, request, queryset):
        for ad in queryset:
            ad.restore()

    enable.description = "Enable User(s)"
    disable.description = "Disable User(s)"
    logical_erase.description = "Delete User(s)"
    restore.description = "Restore User(s)"


@admin.register(HistoricalPurchase)
class HistoricalPurchaseAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "message",
        "invoice",
        "user",
        "deleted",
    ]
    list_display_links = ["uuid"]
    list_filter = ("deleted",)
