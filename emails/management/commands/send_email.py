"""
Django Management Command for Sending Welcome Emails
Usage:
python manage.py send_email -u <user_id_1> <user_id_2> ...
Options:
-u, --user_id: Specify one or more user IDs to send welcome emails to specific users.
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from emails import task


class Command(BaseCommand):
    """
    Custom Django Management Command for Sending Welcome Emails
    """
    help = 'Sends Welcome Email to Users.'

    def add_arguments(self, parser):
        """
        Define command-line arguments for the 'send_email' command.
        -u, --user_id: One or more user IDs to send welcome emails to specific users.
        """
        parser.add_argument('-u', '--user_id', nargs='+', type=int, help='User IDs')

    def handle(self, *args, **kwargs):
        """
        Handle the execution of the 'send_email' command.

        This function sends welcome emails to users based on the provided user IDs.
        If no user IDs are specified, it sends welcome emails to all users in the system.
        """
        users_ids = kwargs['user_id']

        if users_ids:
            for user_id in users_ids:
                try:
                    user = User.objects.get(pk=user_id)
                    task.send_mail_task.delay(user_id)
                    self.stdout.write(f'Sending welcome email to '
                                      f'{user.username} with id {user_id}!')
                except User.DoesNotExist:
                    self.stdout.write(f'User with id {user_id} does not exist.')
        else:
            for user in User.objects.all():
                task.send_mail_task.delay(user.id)
                self.stdout.write(f'Sending welcome email to '
                                  f'{user.username} with id {user.id}!')


