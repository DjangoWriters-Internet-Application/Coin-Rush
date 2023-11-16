import json
from django.core.management.base import BaseCommand
from coinRush.models import CourseCategory, Learn

class Command(BaseCommand):
    help = 'Restore the database data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Restoring data...'))

        # restore logic goes here
        with open('learn_backup.json', 'r') as file:
            backup_data = json.load(file)

        # Restore CourseCategory
        self.restore_model_data(CourseCategory, backup_data['course_categories'])

        # Restore Learn
        self.restore_model_data(Learn, backup_data['learns'])

        self.stdout.write(self.style.SUCCESS('Data restore complete'))

    def restore_model_data(self, model, data):
        # Clear existing data
        model.objects.all().delete()

        # Insert backed up data
        model.objects.bulk_create(
            model(**item) for item in data
        )