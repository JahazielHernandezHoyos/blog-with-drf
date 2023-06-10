from django.contrib import admin

# Register your models here.

admin.site.site_header = "Based API"
admin.site.site_title = "Based API"
admin.site.index_title = "Based API"


class BaseModelAdmin(admin.ModelAdmin):
    actions = ["enable", "disable", "restore", "logical_erase"]

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
