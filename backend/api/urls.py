from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TagViewSet, IngredientViewSet,
                    RecipeViewSet, UserViewSet)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(r'recipes', RecipeViewSet)
router_v1.register(r'tags', TagViewSet)
router_v1.register(r'ingredients', IngredientViewSet)
router_v1.register(r'users', UserViewSet)


urlpatterns = [
    path("auth/", include("djoser.urls.authtoken")),
    path('', include(router_v1.urls)),
]