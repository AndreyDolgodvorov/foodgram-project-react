from django.contrib import admin

from .models import (Favorite, Ingredient, RecipeIngredient,
                     Recipe, ShoppingCart, Tag,)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    list_filter = ('name',)
    search_fields = ('name',)


class IngredientsInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 3
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'pub_date', 'count_favorite',)
    list_filter = ('name', 'author__username', 'tags__name',)
    search_fields = ('name', 'author__username', 'tags__name',)
    readonly_fields = ('favorite',)
    inlines = [IngredientsInline]

    def count_favorite(self, obj):
        return obj.favorite.all().count()

    count_favorite.short_description = 'В избранном'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'recipe__name')
    list_filter = ('user__username',)
    search_fields = ('user__username',)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'recipe__name')
    list_filter = ('user__username',)
    search_fields = ('author',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe__name', 'ingredient__name', 'amount',)
    list_filter = ('recipe__name', 'ingredient__name')
    search_fields = ('recipe__name',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
