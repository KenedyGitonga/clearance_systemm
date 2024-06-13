from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from clearancee.models import Student

class Command(BaseCommand):
    help = 'Create Student instances for users without them'

    def handle(self, *args, **kwargs):
        users_without_students = User.objects.filter(student__isnull=True)
        for user in users_without_students:
            Student.objects.create(user=user, year_of_study=1)
            self.stdout.write(self.style.SUCCESS(f'Created Student for user {user.username}'))