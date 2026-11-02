from django.contrib import admin

from .models import Category, Course, Lesson, Module


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "mentor",
        "status",
        "price",
        "created_at",
    )
    search_fields = ("title", "description")
    list_filter = ("status", "category")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "module",
        "content_type",
        "order",
        "is_preview",
    )
    list_filter = ("content_type", "is_preview")
    search_fields = ("title",)