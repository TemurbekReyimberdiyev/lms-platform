from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, CourseViewSet


router = DefaultRouter()

router.register(
    "categories",
    CategoryViewSet,
    basename="category",
)

router.register(
    "courses",
    CourseViewSet,
    basename="course",
)

urlpatterns = router.urls