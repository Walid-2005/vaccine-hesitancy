from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from pages.models import RespondentsInfo, Responses


class ApiPredictTests(TestCase):
    """
    Unit tests for the predict_hesitancy view endpoint (existing + kept).
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


# ---------- Added: Business-behavior + edge-case tests ----------

class PredictBusinessBehaviorTests(TestCase):
    """
    Asserts that the predict view reflects the user's stored business outcome
    and handles edge conditions around the session user id.
    """

    def setUp(self):
        self.client = Client()
        # Create a separate user with a distinct result label
        self.info_high = RespondentsInfo.objects.create(
            age='30-40',
            sex='Female',
            marital_status='Married',
            no_of_children='1',
            place='Rural',
            qualification='Secondary Education',
            job='Teacher'
        )
        answers = {f'question{i}': 'No' for i in range(1, 31)}
        Responses.objects.create(
            user_id=self.info_high,
            hesitancy_result='High Hesitancy',
            hesitancy_score=15.0,
            **answers
        )

    def test_predict_uses_user_response_label(self):
        """
        With last_user_id set to a user who has a stored response, the
        template context should expose that business result (label).
        """
        session = self.client.session
        session['last_user_id'] = self.info_high.pk
        session.save()

        resp = self.client.get(reverse('predict_hesitancy'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'pages/result.html')
        # Expect your view to surface the result label in context['result'].
        # (If your key is different, tell me and I'll adjust.)
        self.assertIn('result', resp.context)
        self.assertIn('High Hesitancy', str(resp.context['result']))

    def test_invalid_session_user_id_shows_error(self):
        """
        If the session points to a non-existent user, the view should handle gracefully.
        """
        session = self.client.session
        session['last_user_id'] = 999999  # non-existent
        session.save()

        resp = self.client.get(reverse('predict_hesitancy'))
        # Keep behavior consistent with your existing no-session test.
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "No survey data found!")


class SurveySubmissionTests(TestCase):
    """
    Tests for valid survey submission (existing + kept).
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


# ---------- Added: E2E flow (submit -> predict result) ----------

class EndToEndFlowTests(TestCase):
    """
    Full flow: submit survey -> redirect -> predict page renders a result.
    """

    def setUp(self):
        self.client = Client()

    def test_submit_then_predict_renders_result(self):
        payload = {
            "age": "20-30",
            "sex": "Male",
            "marital_status": "Unmarried",
            "no_of_children": "0",
            "place": "Urban",
            "qualification": "Tertiary Education",
            "job": "Student",
        }
        payload.update({f"question{i}": "Yes" for i in range(1, 31)})

        resp = self.client.post(reverse("survey"), data=payload, follow=True)
        # Follow through to prediction page
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'pages/result.html')
        self.assertIn('result', resp.context)


class ModelTests(TestCase):
    """
    Unit tests for model creation and data integrity (existing + kept).
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
    Tests for views that require authentication or admin access (existing + kept).
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
