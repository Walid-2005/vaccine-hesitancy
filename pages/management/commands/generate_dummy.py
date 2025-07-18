"""
Management command to generate dummy survey respondent data.

This command is useful for development, testing, or demonstration purposes.
It inserts random demographic entries into the `RespondentsInfo` table and
links them with a partial `Responses` record.

Usage:
    python manage.py generate_dummy_data [count]

Example:
    python manage.py generate_dummy_data 50
"""

import random
from django.core.management.base import BaseCommand
from pages.models import RespondentsInfo, Responses


class Command(BaseCommand):
    """
    Django management command to generate synthetic respondent and response records.

    Arguments:
        count (int): Number of entries to generate (default = 20)
    """

    help = 'Generate dummy survey data'

    def add_arguments(self, parser):
        """
        Add optional command-line argument to specify the number of records.
        """
        parser.add_argument('count', type=int, nargs='?', default=20)

    def handle(self, *args, **options):
        """
        Create `count` synthetic respondent records with associated Responses.

        The data is randomly generated and not meant for production use.
        """
        count = options['count']

        # Define sample choices for demographic fields
        ages = ['<20', '20-30', '30-50', '>50']
        genders = ['Male', 'Female']
        maritals = ['Unmarried', 'Married']
        children = ['0', '1', '2', '>2']
        places = ['Urban', 'Rural']
        qualifications = [
            'Tertiary Education', 'Primary/Secondary',
            'Higher Secondary', 'Higher Education'
        ]
        jobs = [
            'Business', 'Clerical Job', 'Daily Earners', 'Housewife',
            'Professional (Eg. Teachers, Engineers, Dr. Pharmacist etc)',
            'Student'
        ]

        for _ in range(count):
            # Create respondent with random demographic values
            respondent = RespondentsInfo.objects.create(
                age=random.choice(ages),
                sex=random.choice(genders),
                marital_status=random.choice(maritals),
                no_of_children=random.choice(children),
                place=random.choice(places),
                qualification=random.choice(qualifications),
                job=random.choice(jobs)
            )

            # Create empty response with random hesitancy score (no answers)
            Responses.objects.create(
                user_id=respondent,
                hesitancy_score=random.randint(0, 100)
            )

        self.stdout.write(self.style.SUCCESS(f'✅ {count} dummy records created!'))
