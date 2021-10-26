from rest_framework.routers import DefaultRouter

from calculator.views.products import ProductViewSet

from calculator.views.blackbox import BlackBoxViewSet


router = DefaultRouter()
router.register('product', ProductViewSet)
router.register('black-box', BlackBoxViewSet)

urlpatterns = router.urls
