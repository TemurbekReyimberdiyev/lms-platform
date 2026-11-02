from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Course

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Category name kamida 2 ta belgidan iborat bo'lishi kerak."
            )

        return value

    def validate_slug(self, value):
        value = value.strip().lower()

        if not value:
            raise serializers.ValidationError(
                "Slug bo'sh bo'lishi mumkin emas."
            )

        return value


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_active=True),
        source="category",
        write_only=True,
    )

    mentor_username = serializers.CharField(
        source="mentor.username",
        read_only=True,
    )

    mentor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="mentor"),
        source="mentor",
        write_only=True,
        required=False,
    )

    class Meta:
        model = Course
        fields = [
            "id",
            "category",
            "category_id",
            "mentor_username",
            "mentor_id",
            "title",
            "slug",
            "description",
            "price",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_title(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Kurs nomi kamida 3 ta belgidan iborat bo'lishi kerak."
            )

        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Kurs narxi manfiy bo'lishi mumkin emas."
            )

        return value
    def validate(self, attrs):
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            user = request.user

            is_admin = (
                user.is_superuser
                or user.is_staff
                or user.role == "admin"
            )

            if is_admin and "mentor" not in attrs:
                raise serializers.ValidationError({
                    "mentor_id": "Admin kurs uchun mentor tanlashi kerak."
                })

        return attrs