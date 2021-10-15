from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('product', views.ProductViewSet)
router.register('black-box', views.BlackBoxViewSet)
router.register('item', views.BlackBoxItemViewSet)

urlpatterns = router.urls
