from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.apps import apps

from .forms import PredictionForm
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
