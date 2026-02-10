from rest_framework.routers import DefaultRouter

from employees.views import EmployeeViewSet

router = DefaultRouter()
router.register(r"", EmployeeViewSet, basename="employees")
urlpatterns = router.urls
