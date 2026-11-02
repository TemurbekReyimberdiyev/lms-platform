from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from .models import Category, Course
from .serializers import CategorySerializer, CourseSerializer


class IsPlatformAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        user = request.user

        return (
            user.is_authenticated
            and (user.is_staff or user.role == "admin")
        )


class IsAdminOrMentorOwner(BasePermission):
    """
    Admin barcha kurslarni boshqarishi mumkin.
    Mentor faqat o'z kurslarini boshqarishi mumkin.
    Student va anonymous foydalanuvchilar yozish huquqiga ega emas.
    """

    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        user = request.user

        if not user.is_authenticated:
            return False

        return (
            user.is_superuser
            or user.is_staff
            or user.role in ("admin", "mentor")
        )

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        user = request.user

        if user.is_superuser or user.is_staff or user.role == "admin":
            return True

        return (
            user.role == "mentor"
            and obj.mentor_id == user.id
        )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsPlatformAdminOrReadOnly]


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrMentorOwner]

    def get_queryset(self):
        user = self.request.user

        queryset = Course.objects.select_related(
            "category",
            "mentor",
        )

        if not user.is_authenticated:
            return queryset.filter(
                status=Course.Status.PUBLISHED
            )

        if (
            user.is_superuser
            or user.is_staff
            or user.role == "admin"
        ):
            return queryset

        if user.role == "mentor":
            return queryset.filter(
                mentor=user
            )

        return queryset.filter(
            status=Course.Status.PUBLISHED
        )

    def perform_create(self, serializer):
        user = self.request.user

        if user.role == "mentor":
            serializer.save(mentor=user)
        else:
            serializer.save()