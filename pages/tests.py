from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from pages.models import RespondentsInfo, Responses

# -------------------------------------------------------------------
# 1) View tests
# -------------------------------------------------------------------
class PagesSimpleTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view_renders(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'pages/index.html')

    def test_survey_view_get(self):
        resp = self.client.get(reverse('survey'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'pages/survey_template.html')


# -------------------------------------------------------------------
# 2) Survey submission tests
# -------------------------------------------------------------------
class SurveySubmissionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("survey")  # ✅ Added this line

        self.valid_demo = {
            'age': '20-30',
            'sex': 'Male',
            'marital_status': 'Unmarried',
            'no_of_children': '0',
            'place': 'Urban',
            'qualification': 'Tertiary Education',
            'job': 'Student',
        }

        self.valid_answers = {f'question{i}': 'Yes' for i in range(1, 31)}

    def test_valid_survey_submission_sets_session_and_redirects(self):
        payload = {**self.valid_demo, **self.valid_answers}
        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('predict_hesitancy'))

        session = self.client.session
        self.assertIn('last_user_id', session)
        self.assertIsInstance(session['last_user_id'], int)

    def test_invalid_survey_submission_rerenders_survey_with_errors(self):
        bad_demo = self.valid_demo.copy()
        bad_demo.pop('age')
        payload = {**bad_demo, **self.valid_answers}
        resp = self.client.post(self.url, data=payload)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'pages/survey_template.html')

        session = self.client.session
        self.assertNotIn('last_user_id', session)

        self.assertIn('form1', resp.context)
        form1 = resp.context['form1']
        self.assertTrue(form1.errors)
        self.assertIn('age', form1.errors)


# -------------------------------------------------------------------
# 3) Protected views
# -------------------------------------------------------------------
class ProtectedViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'u@e.com', 'pass')
        self.admin = User.objects.create_superuser('admin', 'a@e.com', 'pass')

    def test_data_view_requires_login(self):
        resp = self.client.get(reverse('data'))
        self.assertEqual(resp.status_code, 302)

    def test_data_view_when_logged_in(self):
        self.client.login(username='testuser', password='pass')
        resp = self.client.get(reverse('data'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'pages/data.html')

    def test_admin_dashboard_requires_login(self):
        resp = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(resp.status_code, 302)

    def test_admin_dashboard_as_regular_user(self):
        self.client.login(username='testuser', password='pass')
        resp = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(resp.status_code, 302)

    def test_admin_dashboard_as_superuser(self):
        self.client.login(username='admin', password='pass')
        resp = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'pages/admin_dashboard.html')


# -------------------------------------------------------------------
# 4) Model-level tests
# -------------------------------------------------------------------
class ModelTests(TestCase):
    def test_respondentsinfo_creation(self):
        info = RespondentsInfo.objects.create(
            age='20-30', sex='Male', marital_status='Unmarried',
            no_of_children='0', place='Urban',
            qualification='Tertiary Education', job='Student'
        )
        self.assertIsNotNone(info.user_id)  # ✅ Use actual primary key field

    def test_responses_requires_user_id(self):
        answers = {f'question{i}': 'Yes' for i in range(1, 31)}
        with self.assertRaises(IntegrityError):
            Responses.objects.create(**answers)

    def test_responses_creation_increments(self):
        info = RespondentsInfo.objects.create(
            age='20-30', sex='Male', marital_status='Unmarried',
            no_of_children='0', place='Urban',
            qualification='Tertiary Education', job='Student'
        )
        before = Responses.objects.count()
        Responses.objects.create(user_id=info, **{f'question{i}': 'Yes' for i in range(1, 31)})
        after = Responses.objects.count()
        self.assertEqual(after, before + 1)
