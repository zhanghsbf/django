from django.test import TestCase
from django.utils import timezone
import datetime
from .models import Question
from django.core.urlresolvers import reverse

class QuestionMethodTests(TestCase):
	def test_was_published_recently_with_future_question(self):
		"""当问题的发布日期在未来的时候，
		was_published_recently函数应当返回False
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertEqual(future_question.was_published_recently(),False)

	def test_was_published_recently_with_recent_question(self):
		"""
		昨天发布的问题应该返回True
		"""
		time = timezone.now() - datetime.timedelta(hours=1)
		recent_question = Question(pub_date=time)
		self.assertTrue(recent_question.was_published_recently())

	def test_was_published_recently_with_old_question(self):
		"""
		一天以前发布的问题应该返回False
		"""
		time = timezone.now() - datetime.timedelta(days=30)
		old_question = Question(pub_date=time)
		self.assertFalse(old_question.was_published_recently())

def create_question(question,days):
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question=question,pub_date=time)

class QuestionViewTests(TestCase):
	def test_index_view_with_no_questions(self):
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'No polls are available.')
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_a_past_question(self):
		create_question(question='Past quesiton', days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question>']
		)

	def test_index_view_with_a_future_question(self):
		create_question(question="Future question", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls are available",
								status_code=200)
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )		