import csv

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps

from .forms import PredictionForm, DoctorVerificationForm
from .models import Prediction

import matlab


def home(request):
    return render(request, 'home.html')


@login_required(login_url='login/')
def prediction_input_view(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)

        if form.is_valid():
            # Extract form data
            data = form.cleaned_data
            data['sex'] = int(data['sex'])
            data['chest_pain_type'] = int(data['chest_pain_type'])
            data['fasting_blood_sugar'] = int(data['fasting_blood_sugar'])
            data['resting_ecg'] = int(data['resting_ecg'])
            data['exercise_angina'] = int(data['exercise_angina'])
            data['st_slope'] = int(data['st_slope'])

            input_data = [
                data['st_slope'], data['age'], data['chest_pain_type'], data['cholesterol'], data['exercise_angina'],
                data['fasting_blood_sugar'], data['max_heart_rate'], data['oldpeak'],  data['resting_bp_s'],
                int(data['resting_ecg']), data['sex']
            ]

            # Make prediction
            predictor = apps.get_app_config('predictions').predictor
            result, confidence = predictor.quadratic_svm_prediction_with_probability(matlab.double([input_data]), nargout=2)
            target = int(result)

            # Save to database
            prediction = Prediction(
                age=data['age'], sex=data['sex'], chest_pain_type=data['chest_pain_type'],
                resting_bp_s=data['resting_bp_s'], cholesterol=data['cholesterol'],
                fasting_blood_sugar=data['fasting_blood_sugar'], resting_ecg=data['resting_ecg'],
                max_heart_rate=data['max_heart_rate'], exercise_angina=data['exercise_angina'],
                oldpeak=data['oldpeak'], st_slope=data['st_slope'], target=target, confidence=confidence,
                created_by=request.user
            )
            prediction.save()

            return render(request, 'predictions/success.html', {'target': target, 'confidence': confidence})
    else:
        form = PredictionForm()

    return render(request, 'predictions/prediction_input.html', {'form': form})


def predictions_list_view(request):
    predictions = Prediction.objects.all().order_by('-created_at')
    return render(request, 'predictions/predictions_list.html', {'predictions': predictions})


def my_predictions(request):
    predictions = Prediction.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'predictions/predictions_list.html', {'predictions': predictions, 'my': True})


def confirm_prediction(request, prediction_id):
    prediction = Prediction.objects.get(id=prediction_id)

    if request.method == 'POST':
        form = DoctorVerificationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            prediction.medical_result = data['result']
            prediction.diagnosis = data['diagnosis']
            if data['result'] == 0:
                prediction.diagnosis = None

            prediction.save()

    return render(request, 'predictions/confirm_prediction.html', {'prediction': prediction, 'form': DoctorVerificationForm()})


@staff_member_required(login_url='login/')
def export_train_data_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=\"test_results.csv\"'

    writer = csv.writer(response)
    writer.writerow(['age', 'sex', 'chest_pain_type', 'resting_bp_s', 'cholesterol', 'fasting_blood_sugar',
                     'resting_ecg', 'max_heart_rate', 'exercise_angina', 'oldpeak', 'st_slope', 'target', 'confidence'])

    # TODO: Export only the predictions confirmed by the user
    for result in Prediction.objects.all():
        writer.writerow([
            result.age,
            result.sex,
            result.chest_pain_type,
            result.resting_bp_s,
            result.cholesterol,
            result.fasting_blood_sugar,
            result.resting_ecg,
            result.max_heart_rate,
            result.exercise_angina,
            result.oldpeak,
            result.st_slope,
            result.target,
            result.confidence
        ])

    return response
