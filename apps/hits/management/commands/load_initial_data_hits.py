# -*- encoding: utf-8 -*-

import csv
import os.path

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.hits.models import Hitmen


def create_user(first_name, last_name, email, raw_password, is_super=False):
    user = User(
        first_name=first_name, last_name=last_name, username=email, email=email,
        is_superuser=is_super, is_staff=is_super
    )
    user.set_password(raw_password)
    user.save()

    return user


class Command(BaseCommand):
    help = "Load initial data on Hits App"

    def handle(self, *args, **options):
        hitmen_records = []

        total_users = User.objects.all().count()
        if total_users == 0:

            # Create The Big Boss
            big_boss_user = create_user(
                first_name='Giuseppi', last_name='Linton', email='giuseppi@gmail.com',
                raw_password='passbigboss', is_super=True
            )
            hitmen_records.append(
                Hitmen(user_id=big_boss_user.id)
            )

            try:
                # Create Hitmens
                path_file = f'{os.path.dirname(__file__)}/../data/hitmens.csv'
                with open(path_file) as csv_file:
                    idx = 0
                    csv_reader = csv.reader(csv_file, delimiter=",")
                    for row in csv_reader:
                        user = create_user(
                            first_name=row[0], last_name=row[1], email=row[2], raw_password=row[3]
                        )
                        if idx < 3:  # Hitmens as boss
                            hitmen_records.append(
                                Hitmen(is_boss=True, user_id=user.id)
                            )
                        else:  # Normal Hitmens
                            hitmen_records.append(
                                Hitmen(user_id=user.id)
                            )
                        idx = idx + 1

                    # Bulk hitmens.
                    Hitmen.objects.bulk_create(hitmen_records)
                    self.stdout.write(self.style.SUCCESS("SUCCESS: Initial data loaded."))
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error Load Hitmens: {str(e)}")
                )
        else:
            self.stdout.write(self.style.WARNING("WARNING: Data already exists."))
