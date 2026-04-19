from django.contrib import admin

from .models import SpecDocument, SpecVersion


class SpecVersionInline(admin.TabularInline):
    model = SpecVersion
    extra = 0


@admin.register(SpecDocument)
class SpecDocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_by", "created_at")
    inlines = [SpecVersionInline]


@admin.register(SpecVersion)
class SpecVersionAdmin(admin.ModelAdmin):
    list_display = ("id", "document", "version_number", "created_at")
