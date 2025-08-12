from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from pages.models import RespondentsInfo, Responses


class ApiPredictTests(TestCase):
    """
    Unit tests for the predict_hesitancy view endpoint.
    """

    def setUp(self):
        self.client = Client()

        # Create a valid respondent and response record
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

        self.resp = Responses.objects.create(
            user_id=self.user_info,
            hesitancy_result='Low Hesitancy',
            hesitancy_score=88.5,
            **answers
        )

        # Set up the session with the respondent's ID
        session = self.client.session
        session['last_user_id'] = self.user_info.pk
        session.save()

    def test_predict_hesitancy_view_get_success(self):
        response = self.client.get(reverse('predict_hesitancy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/result.html')
        self.assertIn('result', response.context)

    def test_predict_hesitancy_view_post_success(self):
        response = self.client.post(reverse('predict_hesitancy'), data={})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/result.html')
        self.assertIn('result', response.context)

    def test_predict_hesitancy_no_session_shows_error(self):
        self.client.session.flush()  # Clear session
        response = self.client.get(reverse('predict_hesitancy'))
        self.assertContains(response, "No survey data found!", status_code=200)


class ModelTests(TestCase):
    """
    Unit tests for model creation and data integrity.
    """

    def test_respondentsinfo_creation(self):
        respondent = RespondentsInfo.objects.create(
            age='30-40',
            sex='Female',
            marital_status='Married',
            no_of_children='2',
            place='Rural',
            qualification='Secondary Education',
            job='Teacher'
        )
        self.assertIsNotNone(respondent.user_id)
        self.assertEqual(respondent.age, '30-40')
        self.assertEqual(respondent.sex, 'Female')

    def test_responses_creation_increments(self):
        respondent = RespondentsInfo.objects.create(
            age='20-30',
            sex='Male',
            marital_status='Unmarried',
            no_of_children='0',
            place='Urban',
            qualification='Tertiary Education',
            job='Student'
        )

        initial_count = Responses.objects.count()

        answers = {f'question{i}': 'Yes' for i in range(1, 31)}
        Responses.objects.create(
            user_id=respondent,
            hesitancy_result='Moderate Hesitancy',
            hesitancy_score=76.3,
            **answers
        )

        self.assertEqual(Responses.objects.count(), initial_count + 1)


class ProtectedViewsTests(TestCase):
    """
    Tests for views that require authentication or admin access.
    """

    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpass'
        )
        self.client.login(username='adminuser', password='adminpass')

    def test_admin_dashboard_as_superuser(self):
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/admin_dashboard.html')

    def test_data_view_when_logged_in(self):
        response = self.client.get(reverse('data'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/data.html')


class SurveySubmissionTests(TestCase):
    """
    Tests for valid survey submission.
    """

    def setUp(self):
        self.client = Client()

    def test_valid_survey_submission_sets_session_and_redirects(self):
        form_data = {
            "age": "20-30",
            "sex": "Male",
            "marital_status": "Unmarried",
            "no_of_children": "0",
            "place": "Urban",
            "qualification": "Tertiary Education",
            "job": "Student",
        }
        for i in range(1, 31):
            form_data[f"question{i}"] = "Yes"

        response = self.client.post(reverse("survey"), data=form_data)

        # Should redirect to prediction view
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("predict_hesitancy"))

        # Should set session key
        session = self.client.session
        self.assertIn("last_user_id", session)
