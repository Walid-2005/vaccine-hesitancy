"""
Form definitions for the Vaccine Hesitancy WebApp.

Includes:
- RespondentsInfoForm: For collecting demographic data
- ResponsesForm: For collecting Likert-scale answers to 30 questions
"""

from django import forms
from .models import RespondentsInfo, Responses


class RespondentsInfoForm(forms.ModelForm):
    """
    Form for collecting respondent demographic information.

    Fields:
        - age
        - sex
        - marital_status
        - no_of_children
        - place
        - qualification
        - job

    Uses predefined choices from the RespondentsInfo model and renders them as dropdowns.
    """
    class Meta:
        model = RespondentsInfo
        fields = ['age', 'sex', 'marital_status', 'no_of_children', 'place', 'qualification', 'job']
        widgets = {
            'age': forms.Select(choices=RespondentsInfo._meta.get_field('age').choices or []),
            'sex': forms.Select(choices=RespondentsInfo._meta.get_field('sex').choices or []),
            'marital_status': forms.Select(choices=RespondentsInfo._meta.get_field('marital_status').choices or []),
            'no_of_children': forms.Select(choices=RespondentsInfo._meta.get_field('no_of_children').choices or []),
            'place': forms.Select(choices=RespondentsInfo._meta.get_field('place').choices or []),
            'qualification': forms.Select(choices=RespondentsInfo._meta.get_field('qualification').choices or []),
            'job': forms.Select(choices=RespondentsInfo._meta.get_field('job').choices or []),
        }


class ResponsesForm(forms.ModelForm):
    """
    Form for collecting responses to 30 Likert-scale vaccine hesitancy questions.

    - Automatically assigns question labels
    - Renders responses as radio buttons with Likert-scale options
    - Excludes system-generated fields (user_id, prediction, score)
    """

    # Human-readable question labels
    question_labels = {
        'question1': "1. Do you agree COVID-19 is an infection/disease?",
        'question2': "2. Do you agree that COVID-19 can be prevented by administering a vaccine?",
        'question3': "3. Do you agree that your information about COVID-19 is accurate?",
        'question4': "4. Do you agree that not only COVID-19 but many other infections are vaccine-preventable?",
        'question5': "5. Do you agree that healthy persons do not need any vaccine for any infection including COVID-19?",
        'question6': "6. Do you agree you can be administered with multiple vaccines to increase your immunity?",
        'question7': "7. Do you agree all the vaccine brands available for COVID-19 work the same?",
        'question8': "8. Do you agree COVID-19 vaccination can be associated with side effects?",
        'question9': "9. Do you agree that touching, sharing food, and talking can spread COVID-19?",
        'question10': "10. Do you agree that a non-vaccinated person is more at risk?",
        'question11': "11. Do you agree with the government COVID-19 vaccine program?",
        'question12': "12. Do you agree to take the COVID-19 vaccine including the booster?",
        'question13': "13. Do you agree the COVID vaccine strengthens the immune system?",
        'question14': "14. Are you willing to vaccinate your elderly and children?",
        'question15': "15. If recovery rates are high, will you still agree to take the vaccine?",
        'question16': "16. The available vaccines are safe and effective.",
        'question17': "17. The COVID vaccine rumors are true.",
        'question18': "18. Do you want to volunteer for clinical trials of new vaccines?",
        'question19': "19. Do side effects stop you from getting vaccinated?",
        'question20': "20. Should vaccination be mandatory?",
        'question21': "21. Do you believe in the steps taken by the Ministry of Health?",
        'question22': "22. Is vaccination the best preventive measure against COVID-19?",
        'question23': "23. Is vaccination prohibited in your religion?",
        'question24': "24. Can supplements replace vaccination?",
        'question25': "25. Is COVID-19 a bioweapon?",
        'question26': "26. Can COVID-19 be treated without medication?",
        'question27': "27. Does an infected person need to quarantine?",
        'question28': "28. Is vaccination a government business?",
        'question29': "29. Do masks/disinfectants help prevent infection, but vaccines are still important?",
        'question30': "30. Does COVID recovery mean no need for vaccination?",
    }

    class Meta:
        model = Responses
        exclude = ['user_id', 'hesitancy_result', 'hesitancy_score']

    def __init__(self, *args, **kwargs):
        """
        Customize form field rendering:
        - Apply labels
        - Render radio buttons with Likert scale
        """
        super().__init__(*args, **kwargs)

        # Standard Likert scale options
        likert_choices = [
            (1, "Strongly Disagree"),
            (2, "Disagree"),
            (3, "Neutral"),
            (4, "Agree"),
            (5, "Strongly Agree"),
        ]

        # Set labels and radio buttons
        for field_name in self.fields:
            if field_name in self.question_labels:
                self.fields[field_name].label = self.question_labels[field_name]
                self.fields[field_name].widget = forms.RadioSelect(choices=likert_choices)
