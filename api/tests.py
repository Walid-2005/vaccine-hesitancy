"""
Unit tests for the api.views.predict_hesitancy endpoint.

Covers:
- Valid GET/POST requests with session data
- Missing session edge case
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.template import TemplateDoesNotExist
from pages.models import RespondentsInfo, Responses


class ApiPredictTests(TestCase):
    """
    Tests for the predict_hesitancy endpoint under normal and edge conditions.
    """

    def setUp(self):
        """
        Prepare a valid respondent and response instance and set the session.
        """
        self.client = Client()

        # Create a valid respondent and associated response
        self.user_info = RespondentsInfo.objects.create(
            age='20-30',
            sex='Male',
            marital_status='Unmarried',
            no_of_children='0',
            place='Urban',
            qualification='Tertiary Education',
            job='Student'
        )
        answers = {f'question{i}': 'Yes' for i in range(1, 31)}
        self.resp = Responses.objects.create(user_id=self.user_info, **answers)

        # Simulate logged-in session with last_user_id
        session = self.client.session
        session['last_user_id'] = self.user_info.pk
        session.save()

    def test_predict_hesitancy_view_get_success(self):
        """
        Should return status 200 and render result template on GET.
        """
        url = reverse('predict_hesitancy')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/result.html')
        self.assertIn('result', response.context)

    def test_predict_hesitancy_view_post_success(self):
        """
        Should return status 200 and render result template on POST.
        """
        url = reverse('predict_hesitancy')
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/result.html')
        self.assertIn('result', response.context)

    def test_predict_hesitancy_no_session_raises(self):
        """
        If no last_user_id is in session, the view should try to render an error page.

        Since 'error.html' does not exist in the test setup, it should raise TemplateDoesNotExist.
        """
        self.client.session.flush()
        url = reverse('predict_hesitancy')
        with self.assertRaises(TemplateDoesNotExist):
            self.client.get(url)
