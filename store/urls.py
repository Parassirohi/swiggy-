
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('products', views.ProductViewSet)
router.register('sellers', views.SellerViewSet)
router.register('customers', views.CustomerViewSet)

urlpatterns = router.urls
