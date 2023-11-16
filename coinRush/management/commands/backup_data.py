import json
from django.core.management.base import BaseCommand
from coinRush.models import CourseCategory, Learn

class Command(BaseCommand):
    help = 'Backup the database data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Backing up data...'))

        # Backup CourseCategory
        course_categories = list(CourseCategory.objects.values())

        # Backup Learn
        learns = list(Learn.objects.values())

        # Save the backup to a file
        with open('learn_backup.json', 'w') as file:
            json.dump({
                'course_categories': course_categories,
                'learns': learns,
            }, file, indent=2)

        self.stdout.write(self.style.SUCCESS('Data backup complete'))