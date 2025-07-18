"""
Django model definitions for the Vaccine Hesitancy WebApp.

Includes:
- RespondentsInfo: demographic metadata for survey participants
- Responses: answer fields for 30 survey questions and prediction outputs
"""

from django.db import models


class RespondentsInfo(models.Model):
    """
    Stores demographic information about a survey respondent.

    Fields:
        - user_id (AutoField): Primary key
        - age, sex, marital_status, etc.: Categorical fields with predefined choices
    """

    # Predefined choices for categorical fields
    AGE_CHOICES = [('<20', '<20'), ('20-30', '20-30'), ('30-50', '30-50'), ('>50', '>50')]
    SEX_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    MARITAL_CHOICES = [('Unmarried', 'Unmarried'), ('Married', 'Married')]
    CHILDREN_CHOICES = [('0', '0'), ('1', '1'), ('2', '2'), ('>2', '>2')]
    PLACE_CHOICES = [('Urban', 'Urban'), ('Rural', 'Rural')]
    QUALIFICATION_CHOICES = [
        ('Tertiary Education', 'Tertiary Education'),
        ('Primary/Secondary', 'Primary/Secondary'),
        ('Higher Secondary', 'Higher Secondary'),
        ('Higher Education', 'Higher Education')
    ]
    JOB_CHOICES = [
        ('Business', 'Business'),
        ('Clerical Job', 'Clerical Job'),
        ('Daily Earners', 'Daily Earners'),
        ('Housewife', 'Housewife'),
        ('Professional (Eg. Teachers, Engineers, Dr. Pharmacist etc)', 'Professional (Eg. Teachers, Engineers, Dr. Pharmacist etc)'),
        ('Student', 'Student')
    ]

    user_id = models.AutoField(db_column='UserID', primary_key=True)
    age = models.CharField(max_length=5, choices=AGE_CHOICES)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_CHOICES)
    no_of_children = models.CharField(max_length=10, choices=CHILDREN_CHOICES)
    place = models.CharField(max_length=10, choices=PLACE_CHOICES)
    qualification = models.CharField(max_length=50, choices=QUALIFICATION_CHOICES)
    job = models.CharField(max_length=100, choices=JOB_CHOICES)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        db_table = 'respondents_info'  # Removed 'managed = False'


class Responses(models.Model):
    """
    Stores answers to 30 Likert-scale survey questions and AI-generated results.

    Fields:
        - user_id (OneToOne): Links to a respondent
        - question1 through question30: Response fields
        - hesitancy_result: Categorical prediction by ML model
        - hesitancy_score: Numeric score generated from responses
    """

    user_id = models.OneToOneField(RespondentsInfo, db_column='UserID', primary_key=True, on_delete=models.CASCADE)

    # Survey response fields (text like 'Yes', 'No', etc.)
    question1 = models.CharField(db_column='Question1', max_length=20)
    question2 = models.CharField(db_column='Question2', max_length=20)
    question3 = models.CharField(db_column='Question3', max_length=20)
    question4 = models.CharField(db_column='Question4', max_length=20)
    question5 = models.CharField(db_column='Question5', max_length=20)
    question6 = models.CharField(db_column='Question6', max_length=20)
    question7 = models.CharField(db_column='Question7', max_length=20)
    question8 = models.CharField(db_column='Question8', max_length=20)
    question9 = models.CharField(db_column='Question9', max_length=20)
    question10 = models.CharField(db_column='Question10', max_length=20)
    question11 = models.CharField(db_column='Question11', max_length=20)
    question12 = models.CharField(db_column='Question12', max_length=20)
    question13 = models.CharField(db_column='Question13', max_length=20)
    question14 = models.CharField(db_column='Question14', max_length=20)
    question15 = models.CharField(db_column='Question15', max_length=20)
    question16 = models.CharField(db_column='Question16', max_length=20)
    question17 = models.CharField(db_column='Question17', max_length=20)
    question18 = models.CharField(db_column='Question18', max_length=20)
    question19 = models.CharField(db_column='Question19', max_length=20)
    question20 = models.CharField(db_column='Question20', max_length=20)
    question21 = models.CharField(db_column='Question21', max_length=20)
    question22 = models.CharField(db_column='Question22', max_length=20)
    question23 = models.CharField(db_column='Question23', max_length=20)
    question24 = models.CharField(db_column='Question24', max_length=20)
    question25 = models.CharField(db_column='Question25', max_length=20)
    question26 = models.CharField(db_column='Question26', max_length=20)
    question27 = models.CharField(db_column='Question27', max_length=20)
    question28 = models.CharField(db_column='Question28', max_length=20)
    question29 = models.CharField(db_column='Question29', max_length=20)
    question30 = models.CharField(db_column='Question30', max_length=20)

    # AI model output fields
    hesitancy_result = models.CharField(db_column='HesitancyResult', max_length=20, null=True, blank=True)
    hesitancy_score = models.FloatField(db_column='HesitancyScore', null=True, blank=True)

    class Meta:
        db_table = 'responses'
