from djoser.views import UserViewSet as DjoserUserViewSet
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeWriteSerializer,
                          FavoriteSerializer, ShoppingCartSerializer,
                          UserSerializer, FollowSerializer)
from recipes.models import (Tag, Ingredient, Recipe,
                            RecipeIngredient, Favorite, ShoppingCart)
from users.models import Follow
from .permissions import (IsOwnerOrAdminOrReadOnly,
                          IsCurrentUserOrAdminOrReadOnly)

from .filters import IngredientSearchFilter, RecipeFilter
from .paginations import CustomPagination

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsOwnerOrAdminOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsOwnerOrAdminOrReadOnly,)
    filter_backends = (IngredientSearchFilter, )
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    pagination_class = CustomPagination
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    # def add_del_recipe(self, model, serializer_class):
    #     recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
    #     user = self.request.user
    #     if self.request.method == 'POST':
    #         if model.objects.filter(user=user,
    #                                 recipe=recipe).exists():
    #             return Response({'errors': 'Рецепт уже добавлен.'},
    #                             status=status.HTTP_400_BAD_REQUEST)
    #         serializer = serializer_class(data=self.request.data)
    #         if serializer.is_valid(raise_exception=True):
    #             serializer.save(user=user, recipe=recipe)
    #             return Response(serializer.data,
    #                             status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)
    #     if not model.objects.filter(user=user,
    #                                 recipe=recipe).exists():
    #         return Response({'errors': 'Рецепт не найден.'},
    #                         status=status.HTTP_404_NOT_FOUND)
    #     model.objects.get(recipe=recipe).delete()
    #     return Response('Рецепт удалён из избранного.',
    #                     status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['POST'],
            permission_classes=[IsAuthenticated])
    def add_recipe(self, model, serializer_class):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        user = self.request.user
        if model.objects.filter(user=user,
                                recipe=recipe).exists():
            return Response({'errors': 'Рецепт уже добавлен.'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = serializer_class(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user, recipe=recipe)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=['DELETE'],
            permission_classes=[IsAuthenticated])
    def del_recipe(self, model):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        user = self.request.user
        if not model.objects.filter(user=user,
                                    recipe=recipe).exists():
            return Response({'errors': 'Рецепт не найден.'},
                            status=status.HTTP_404_NOT_FOUND)
        model.objects.get(recipe=recipe).delete()
        return Response('Рецепт удалён.',
                        status=status.HTTP_204_NO_CONTENT)

    def favorite(self, request, **kwargs):
        if self.request.method == 'POST':
            return self.del_recipe(Favorite, FavoriteSerializer)
        return self.del_recipe(Favorite)
        
    def shopping_cart(self, request, **kwargs):
        if self.request.method == 'POST':
            return self.del_recipe(ShoppingCart, ShoppingCartSerializer)
        return self.del_recipe(ShoppingCart)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = self.request.user
        if not user.shopping_cart.exists():
            return Response('Список покупок пуст.',
                            status=status.HTTP_204_NO_CONTENT)
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            amount=Sum('amount')
        ).order_by('amount')
        shopping_list = []
        for ingredient in ingredients:
            shopping_list += (
                f'{ingredient["ingredient__name"].capitalize()} '
                f'({ingredient["ingredient__measurement_unit"]}) — '
                f'{ingredient["amount"]}\n'
            )
        filename = 'shopping_list.txt'
        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsCurrentUserOrAdminOrReadOnly, )
    pagination_class = CustomPagination

    @action(methods=['get'],
            detail=False,
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = self.request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    @action(['POST'],
            detail=False,
            permission_classes=[IsAuthenticated])
    def set_password(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(
            data=request.data,
            context={'request': request})
        if serializer.is_valid(raise_exception=True):
            self.request.user.set_password(serializer.data["new_password"])
            self.request.user.save()
            return Response('Пароль успешно изменен',
                            status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            if Follow.objects.filter(author=author, user=user).exists():
                return Response({'error': 'Вы уже подписаны'},
                                status=status.HTTP_400_BAD_REQUEST)
            if user == author:
                return Response({'error': 'Невозможно подписаться на себя'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = FollowSerializer(author, context={'request': request})
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if Follow.objects.filter(author=author, user=user).exists():
            Follow.objects.filter(author=author, user=user).delete()
            return Response('Подписка удалена',
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Вы не подписаны на этого пользователя'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            methods=['GET'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        follows = User.objects.filter(following__user=user)
        page = self.paginate_queryset(follows)
        serializer = FollowSerializer(
            page, many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)
