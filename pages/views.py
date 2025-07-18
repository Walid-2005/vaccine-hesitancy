"""
Views for handling survey submission, authentication, admin dashboard, and data export
for the Vaccine Hesitancy WebApp.

This module includes:
- Public views for survey and result rendering
- Authenticated views for admin and data download
- Form handling and session storage
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Responses, RespondentsInfo
from .forms import RespondentsInfoForm, ResponsesForm
import openpyxl
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Prefetch
import pandas as pd


def index(request):
    """
    Render the home page.
    """
    return render(request, 'pages/index.html')


def survey_view(request):
    """
    Handle display and submission of the vaccine hesitancy survey form.

    - On GET: display empty forms
    - On POST: validate and save Respondent and Response data
    - Store user ID in session for prediction
    """
    print("Request method:", request.method)

    if request.method == "POST":
        respondent_form = RespondentsInfoForm(request.POST)
        responses_form = ResponsesForm(request.POST)

        if respondent_form.is_valid() and responses_form.is_valid():
            respondent = respondent_form.save()
            responses = responses_form.save(commit=False)
            responses.user_id = respondent  # Link response to respondent
            responses.save()

            # Save user ID to session for result page
            request.session['last_user_id'] = respondent.user_id
            return redirect('predict_hesitancy')
    else:
        respondent_form = RespondentsInfoForm()
        responses_form = ResponsesForm()

    return render(request, "pages/survey_template.html", {
        "form1": respondent_form,
        "form2": responses_form,
    })


@staff_member_required
def admin_dashboard(request):
    """
    Admin-only dashboard view to display summarized survey responses.

    Retrieves responses with respondent info and structures them as JSON
    for use in front-end visualizations (charts, tables).
    """
    responses = Responses.objects.select_related('user_id').all()
    data = []

    for r in responses:
        if r.user_id:
            d = {
                "age": r.user_id.age,
                "sex": r.user_id.sex,
                "place": r.user_id.place,
                "qualification": r.user_id.qualification,
                "hesitancy_score": r.hesitancy_score,
                "predicted_hesitancy": r.hesitancy_result,
                "marital_status": r.user_id.marital_status,
                "no_of_children": r.user_id.no_of_children,
            }
            # Include all question responses
            for i in range(1, 31):
                d[f"question{i}"] = getattr(r, f"question{i}", None)
            data.append(d)

    df = pd.DataFrame(data)
    context = {
        "data": df.to_json(orient="records")
    }
    return render(request, "pages/admin_dashboard.html", context)


def thank_you_view(request):
    """
    Render a simple thank-you page after survey submission.
    """
    return render(request, 'pages/thank_you.html')


def result_view(request):
    """
    Render the page for showing predicted hesitancy results.
    """
    return render(request, "pages/result.html")


def login(request):
    """
    Custom login view.

    - On POST: authenticate user and redirect to data page
    - On GET: render login form
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('data')
        else:
            error_message = "Invalid username or password"
            return render(request, 'pages/login.html', {'error_message': error_message})

    return render(request, 'pages/login.html')


def user_logout(request):
    """
    Logout the current user and redirect to login page.
    """
    logout(request)
    return redirect('login')


@login_required
def data(request):
    """
    Display all stored respondent and response records to authenticated users.
    """
    data_items = RespondentsInfo.objects.select_related('responses').all()
    return render(request, 'pages/data.html', {'data_items': data_items})


@login_required
def download_excel(request):
    """
    Generate and download an Excel file of all survey responses.

    - Uses openpyxl to build the workbook
    - Appends headers and data row-by-row
    - Links each respondent to their associated survey answers
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Survey Responses"

    # Column headers for survey data
    headers = [
        "ID", "Age", "Sex", "Marital Status", "No of Children", "Place", "Qualification", "Job",
    ] + [f"{i}.{q}" for i, q in enumerate([
        "Do you agree COVID-19 is an infection/disease?",
        "Do you agree that COVID-19 can be prevented by administering a vaccine?",
        "Do you agree that your information about COVID-19 is accurate?",
        "Do you agree that not only COVID-19 but many other infections are vaccine-preventable?",
        "Do you agree that healthy persons do not need any vaccine for any infection including COVID-19?",
        "Do you agree that you can be administered with multiple vaccines to increase your immunity?",
        "Do you agree all the vaccine brands available for COVID-19 work the same?",
        "Do you agree that COVID-19 vaccination can be associated with the risk of side effects?",
        "Do you agree that touching, sharing food, and talking can be reasons for the transmission of the COVID virus?",
        "Do you agree that a non-vaccinated person is more at risk than a vaccinated person?",
        "Do you agree with the government COVID-19 vaccine program?",
        "Do you agree to take the COVID-19 vaccine including the booster?",
        "Do you agree that the COVID vaccine will strengthen the immune system?",
        "Are you willing to vaccinate your elderly and children?",
        "If under any COVID-like pandemic, the nation experiences a growing recovery rate, will you agree to take the COVID-19 vaccine?",
        "The available vaccines are safe and effective.",
        "The COVID vaccine rumors are true.",
        "Do you want to volunteer for the clinical trials of new vaccines?",
        "Do the side effects of the vaccine resist you from taking the vaccines?",
        "Should vaccination be mandatory?",
        "Do you believe in the steps taken by the Ministry of Health about the vaccination process?",
        "Is the best preventive measure against COVID-19 vaccination?",
        "Is vaccination prohibited in your religion?",
        "Can eating supplements help prevent coronavirus infection, hence no need for a vaccine?",
        "Is COVID-19 not a virus but a bioweapon?",
        "Can coronavirus be treated without medication?",
        "Does a coronavirus-infected person not need to quarantine themselves?",
        "Is the vaccination process a business for the government?",
        "Does the use of masks/disinfectants help prevent COVID-19 infection, but still, a vaccine is important?",
        "Once a patient recovers from COVID-19, does that mean they do not need vaccination to prevent subsequent infection?",
    ], 1)] + ["Predicted Hesitancy", "Hesitancy Score"]

    ws.append(headers)

    data_items = RespondentsInfo.objects.select_related('responses').all()

    for respondent in data_items:
        response = respondent.responses
        row = [
            respondent.user_id, respondent.age, respondent.sex, respondent.marital_status,
            respondent.no_of_children, respondent.place, respondent.qualification, respondent.job,
        ]
        for i in range(1, 31):
            row.append(getattr(response, f"question{i}", "N/A") if response else "N/A")
        row.append(response.hesitancy_result if response else "N/A")
        row.append(response.hesitancy_score if response else "N/A")
        ws.append(row)

    # Stream the Excel file to the client
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=survey_responses.xlsx"
    wb.save(response)
    return response
