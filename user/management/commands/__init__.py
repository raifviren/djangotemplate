"""
Created at 11/07/20
@author: virenderkumarbhargav
"""
from itertools import chain

from django.core.management.base import BaseCommand, CommandError
import traceback
from user.models import *


class Command(BaseCommand):
    help = 'This command will correct the  reply_count and post_count of every user.'

    def handle(self, *args, **options):
        try:
            pass
            # users= User.objects.all()
            # for user in users:
            #     feed_count = Feed.objects.filter(created_by=user).count()
            #     user.post_count = feed_count
            #     feed_comment_count = FeedComment.objects.filter(created_by=user).count()
            #     story_comment_count = StoryComment.objects.filter(created_by=user).count()
            #     blog_comment_count = BlogComment.objects.filter(created_by=user).count()
            #     user.reply_count =  feed_comment_count + story_comment_count + blog_comment_count
            #     user.save()
            #     self.stdout.write(self.style.SUCCESS('done for:'+ str(user)))
        except Exception as e :
            traceback.print_exc(e)
        self.stdout.write(self.style.SUCCESS('Command is successfully executed.'))