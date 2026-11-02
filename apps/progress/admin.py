from django.contrib import admin

from .models import LessonProgress


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "lesson",
        "is_completed",
        "last_position_seconds",
        "updated_at",
    )
    list_filter = ("is_completed",)
    search_fields = (
        "student__username",
        "lesson__title",
    )