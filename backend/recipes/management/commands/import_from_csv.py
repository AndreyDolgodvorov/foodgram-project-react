import csv

from django.core.management.base import BaseCommand
from ...models import (Ingredient)


class Command(BaseCommand):
    def handle(self, **options):
        Ingredient.objects.all().delete()
        with open(r'backend\data\ingredients.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1],
                )
