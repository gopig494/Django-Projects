import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Book


class BookModelTests(TestCase):
    def test_s(self):
        # print("--------------------------------tests")
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        # print("-------------------------timezone.now()",timezone.now())
        # print("-------------------------datetime-30",datetime.timedelta(days=30))
        # print("-------------------------datetime-++--",timezone.now() + datetime.timedelta(days=30))

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Book(published_date=time)
        # print("------------future_question",future_question)
        # print("------------assertIs", self.assertIs(future_question.was_published_recently(), True))
        self.assertIs(future_question.was_published_recently(), True)
