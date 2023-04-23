import csv

from django.core.management.base import BaseCommand
from django.conf import settings
from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        Ingredient.objects.all().delete()
        with open(r'data\ingredients.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1],
                )
