# your_app/management/commands/backup_data.py

import json
import os
from django.core.management.base import BaseCommand
from coinRush.models import CourseCategory, Learn

class Command(BaseCommand):
    help = 'Backup the database data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Backing up data...'))

        # Backup CourseCategory
        course_categories = list(CourseCategory.objects.values())

        # Backup Learn
        learns = list(self.backup_learn())

        # Save the backup to a file
        with open('backup.json', 'w') as file:
            json.dump({
                'course_categories': course_categories,
                'learns': learns,
            }, file, indent=2)

        self.stdout.write(self.style.SUCCESS('Data backup complete'))

    def backup_learn(self):
        learns_data = []
        for learn in Learn.objects.all():
            # Get the relative path of the image within the app directory
            image_relative_path = os.path.relpath(learn.image.path, 'coinRush/static/images/topic_images/')

            learns_data.append({
                'title': learn.title,
                'description': learn.description,
                'category': learn.category_id,
                'slug': learn.slug,
                'image': image_relative_path,  # Include relative image path
            })

        return learns_data
