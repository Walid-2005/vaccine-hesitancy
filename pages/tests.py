"""
Unit tests for the pages app in the Vaccine Hesitancy WebApp.

Covers:
- Public view rendering
- Survey form submission logic
- Session management
- Access control on protected views
- Basic model integrity tests
"""

from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from pages.models import RespondentsInfo, Responses


# -------------------------------------------------------------------
# 1) View tests that don’t touch the DB
# -------------------------------------------------------------------
class PagesSimpleTests(SimpleTestCase):
    """
    Tests for rendering simple pages that do not involve the database.
    """
    def setUp(self):
        self.client = Client()

    def test_index_view_renders(self):
        """
        Ensure the index view loads successfully and uses the correct template.
        """
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'pages/index.html')

    def test_survey_view_get(self):
        """
        Ensure the survey page loads successfully via GET request.
        """
        resp = self.client.get(reverse('survey'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'pages/survey_template.html')


# -------------------------------------------------------------------
# 2) Survey submission tests
# -------------------------------------------------------------------
class SurveySubmissionTests(TestCase):
    """
    Verify that submitting the survey sets session correctly on valid data,
    and re-renders the form with errors on invalid submission.
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('survey')

        # Minimal valid demographic payload
        self.valid_demo = {
            'age': '20-30',
            'sex': 'Male',
            'marital_status': 'Unmarried',
            'no_of_children': '0',
            'place': 'Urban',
            'qualification': 'Tertiary Education',
            'job': 'Student',
        }

        # Minimal valid answers
        self.valid_answers = {f'question{i}': 'Yes' for i in range(1, 31)}

    def test_valid_survey_submission_sets_session_and_redirects(self):
        """
        Test that valid submission stores user ID in session and redirects to prediction.
        """
        payload = {**self.valid_demo, **self.valid_answers}
        resp = self.client.post(self.url, data=payload)

        # Expect redirect to prediction page
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse('predict_hesitancy'))

        # Verify session variable was set
        session = self.client.session
        self.assertIn('last_user_id', session)
        self.assertIsInstance(session['last_user_id'], int)

    def test_invalid_survey_submission_rerenders_survey_with_errors(self):
        """
        Test that incomplete survey data causes form errors and no session set.
        """
        bad_demo = self.valid_demo.copy()
        bad_demo.pop('age')  # Remove required field

        payload = {**bad_demo, **self.valid_answers}
        resp = self.client.post(self.url, data=payload)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'pages/survey_template.html')

        # Session should not be set
        session = self.client.session
        self.assertNotIn('last_user_id', session)

        # Form should include errors
        self.assertIn('form1', resp.context)
        form1 = resp.context['form1']
        self.assertTrue(form1.errors)
        self.assertIn('age', form1.errors)


# -------------------------------------------------------------------
# 3) Protected views: data & admin_dashboard
# -------------------------------------------------------------------
class ProtectedViewsTests(TestCase):
    """
    Ensure that access to protected views like 'data' and 'admin_dashboard'
    are restricted properly based on authentication and permissions.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'u@e.com', 'pass')
        self.admin = User.objects.create_superuser('admin', 'a@e.com', 'pass')

    def test_data_view_requires_login(self):
        """
        Access to /data should redirect unauthenticated users.
        """
        resp = self.client.get(reverse('data'))
        self.assertEqual(resp.status_code, 302)

    def test_data_view_when_logged_in(self):
        """
        Authenticated users should access /data successfully.
        """
        self.client.login(username='testuser', password='pass')
        resp = self.client.get(reverse('data'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'pages/data.html')

    def test_admin_dashboard_requires_login(self):
        """
        Unauthenticated access to /admin_dashboard should redirect.
        """
        resp = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(resp.status_code, 302)

    def test_admin_dashboard_as_regular_user(self):
        """
        Regular authenticated users should not access /admin_dashboard.
        """
        self.client.login(username='testuser', password='pass')
        resp = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(resp.status_code, 302)

    def test_admin_dashboard_as_superuser(self):
        """
        Admin users should successfully access /admin_dashboard.
        """
        self.client.login(username='admin', password='pass')
        resp = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'pages/admin_dashboard.html')


# -------------------------------------------------------------------
# 4) Model-level tests
# -------------------------------------------------------------------
class ModelTests(TestCase):
    """
    Test data model integrity for RespondentsInfo and Responses.
    """
    def test_respondentsinfo_creation(self):
        """
        Ensure a RespondentsInfo instance can be saved successfully.
        """
        info = RespondentsInfo.objects.create(
            age='20-30', sex='Male', marital_status='Unmarried',
            no_of_children='0', place='Urban',
            qualification='Tertiary Education', job='Student'
        )
        self.assertIsNotNone(info.pk)

    def test_responses_requires_user_id(self):
        """
        Responses without a user_id should raise an IntegrityError.
        """
        answers = {f'question{i}': 'Yes' for i in range(1, 31)}
        with self.assertRaises(IntegrityError):
            Responses.objects.create(**answers)

    def test_responses_creation_increments(self):
        """
        Verify that a valid Responses instance is saved and count increases.
        """
        info = RespondentsInfo.objects.create(
            age='20-30', sex='Male', marital_status='Unmarried',
            no_of_children='0', place='Urban',
            qualification='Tertiary Education', job='Student'
        )
        before = Responses.objects.count()
        resp = Responses.objects.create(user_id=info, **{f'question{i}': 'Yes' for i in range(1, 31)})
        after = Responses.objects.count()
        self.assertEqual(after, before + 1)
