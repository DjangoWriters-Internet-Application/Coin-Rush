import json
from django.core.management.base import BaseCommand
from coinRush.models import CourseCategory, Learn
from django.core.files.base import ContentFile
import os

class Command(BaseCommand):
    help = 'Restore the database data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Restoring data...'))

        # Your restore logic goes here
        with open('backup.json', 'r') as file:
            backup_data = json.load(file)

        # Restore CourseCategory
        self.restore_model_data(CourseCategory, backup_data['course_categories'])

        # Restore Learn
        self.restore_learn_data(backup_data['learns'])

        self.stdout.write(self.style.SUCCESS('Data restore complete'))

    def restore_model_data(self, model, data):
        # Clear existing data
        model.objects.all().delete()

        # Insert backed up data
        model.objects.bulk_create(
            model(**item) for item in data
        )

    def restore_learn_data(self, learns_data):
        for learn_data in learns_data:
            # Get the full path to the image within the app directory
            image_path = os.path.join('coinRush/static/images/topic_images/', learn_data.get('image', ''))

            # Read the image file and save it to the Learn model
            with open(image_path, 'rb') as image_file:
                image_content = ContentFile(image_file.read(), name=os.path.basename(image_path))

            # Restore Learn with image data
            Learn.objects.create(
                title=learn_data['title'],
                description=learn_data['description'],
                category_id=learn_data['category'],
                slug=learn_data['slug'],
                image=image_content,
            )
