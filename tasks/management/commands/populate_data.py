from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from tasks.models import Task, Category, Priority, Note, SubTask

class Command(BaseCommand):
    help = 'Populate database with fake data'
    
    def handle(self, *args, **options):
        fake = Faker()
    
        Category.objects.get_or_create(name=c)
        
        # Get all priorities and categories
        all_priorities = list(Priority.objects.all())
        all_categories = list(Category.objects.all())

        if not all_priorities:
            self.stdout.write(self.style.ERROR('No priorities found. Please add them manually first.'))
            return
            
        if not all_categories:
            self.stdout.write(self.style.ERROR('No categories found. Please add them manually first.'))
            return
        
        # Create Tasks
        for _ in range(50):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                priority=fake.random_element(elements=all_priorities),
                category=fake.random_element(elements=all_categories)
            )
            
            # Create Subtasks for this task
            for _ in range(fake.random_int(min=0, max=5)):
                SubTask.objects.create(
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                    task=task
                )
            
            # Create Notes for this task
            for _ in range(fake.random_int(min=0, max=3)):
                Note.objects.create(
                    content=fake.paragraph(nb_sentences=2),
                    task=task
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with fake data'))