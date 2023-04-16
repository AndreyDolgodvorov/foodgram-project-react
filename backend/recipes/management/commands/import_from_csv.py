import csv

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from ...models import (Ingredient)


class Command(BaseCommand):
    def handle(self, **options):
        Ingredient.objects.all().delete()
        with open(r'static\data\ingredients.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1],
                )
