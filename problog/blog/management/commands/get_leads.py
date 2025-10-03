import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone

from blog.models import Post, Comment


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--all', dest='is_all', action='store_true')
        parser.add_argument('--weeks-since', dest='since', type=int, required=False)
        parser.add_argument('--for-post', dest='post_id', type=int, required=False)
    
    def handle(self, *args, **options):
        is_all = options.get('is_all', False)
        weeks = options.get('since', None)
        post_id = options.get('post_id', None)
        post = None
        if post_id:
            try:
                post = Post.objects.get(
                    id=post_id
                )
            except Post.DoesNotExist:
                self.stderr.write(f'Post ID #{post_id} does not refer to any post in the database.')
                return False
        comments = Comment.objects.filter(active=True)
        if post:
            comments = comments.filter(post=post)
        if weeks:
            date_added = timezone.now().today() - datetime.timedelta(days=7 * weeks)
            comments = comments.filter(
                created__date__gte=date_added
            )
        if comments:
            duplicates = 0
            emails = []
            for comment in comments:
                data = (comment.name, comment.email)
                if data[1] in emails:
                    duplicates += 1
                    continue
                emails.append(data)
            self.stdout.write(f'Arranged personal data from comments meeting your criteria into list. Found {len(emails)} unique leads, not counting the {duplicates} duplicate records that were discarded.')
            self.stdout.write('\n\n\n')
            self.stdout.write(f'Lead Info from Blog Comments\n{"-"*25}\n\n')
            for email in emails:
                self.stdout.write(f'|{email[0].title()}| - {email[1]}\n{"-"*25}')
            self.stdout.write(f'\n\nFinished. Aborting...')
            return True

        else:
            self.stdout.write(f'Your criteria for post comments did not return any data, please broaden your criteria before trying again.')
            return False

            