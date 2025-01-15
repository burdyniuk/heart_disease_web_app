from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.apps import apps

from .forms import PredictionForm
from .models import Prediction
import prediction_model_function as prediction_model

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

            input_data = [
                data['age'], int(data['sex']), int(data['chest_pain_type']), data['resting_bp_s'],
                data['cholesterol'], int(data['fasting_blood_sugar']), int(data['resting_ecg']),
                data['max_heart_rate'], int(data['exercise_angina']), data['oldpeak'], int(data['st_slope'])
            ]

            # Make prediction
            predictor = apps.get_app_config('predictions').predictor
            result = predictor.prediction_model_function(matlab.double([input_data]))
            target = int(result)
            predictor.terminate()

            # Save to database
            prediction = Prediction(
                age=data['age'], sex=int(data['sex']), chest_pain_type=int(data['chest_pain_type']),
                resting_bp_s=data['resting_bp_s'], cholesterol=data['cholesterol'],
                fasting_blood_sugar=int(data['fasting_blood_sugar']), resting_ecg=int(data['resting_ecg']),
                max_heart_rate=data['max_heart_rate'], exercise_angina=int(data['exercise_angina']),
                oldpeak=data['oldpeak'], st_slope=int(data['st_slope']), target=target,
                created_by=request.user
            )
            prediction.save()

            return render(request, 'predictions/success.html', {'target': target})
    else:
        form = PredictionForm()

    return render(request, 'predictions/prediction_input.html', {'form': form})


def predictions_list_view(request):
    predictions = Prediction.objects.all()
    return render(request, 'predictions/predictions_list.html', {'predictions': predictions})


def my_predictions(request):
    predictions = Prediction.objects.filter(created_by=request.user)
    return render(request, 'predictions/predictions_list.html', {'predictions': predictions, 'my': True})
