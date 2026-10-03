from rest_framework.routers import DefaultRouter
from .views import AddTransactionViewSet

router = DefaultRouter()
router.register('transactions',AddTransactionViewSet)
urlpatterns = router.urls