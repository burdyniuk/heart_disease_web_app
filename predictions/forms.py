from django import forms

from predictions.models import Prediction


class PredictionForm(forms.Form):
    age = forms.IntegerField(label='Age')
    sex = forms.ChoiceField(label='Sex', choices=[(0, 'Female'), (1, 'Male')])
    chest_pain_type = forms.ChoiceField(
        label='Chest Pain Type',
        choices=[(1, 'Typical Angina'), (2, 'Atypical Angina'), (3, 'Non-anginal Pain'), (4, 'Asymptomatic')]
    )
    resting_bp_s = forms.IntegerField(label='Resting BP Systolic')
    cholesterol = forms.IntegerField(label='Cholesterol')
    fasting_blood_sugar = forms.ChoiceField(
        label='Fasting Blood Sugar > 120 mg/dl',
        choices=[(0, 'False'), (1, 'True')]
    )
    resting_ecg = forms.ChoiceField(
        label='Resting ECG results',
        choices=[
            (0, 'Normal'),
            (1, 'having ST-T wave abnormality'),
            (2, "showing probable or definite left ventricularhypertrophy by Estes' criteria")
        ]
    )
    max_heart_rate = forms.IntegerField(label='Max Heart Rate')
    exercise_angina = forms.ChoiceField(label='Exercise Angina', choices=[(0, 'No'), (1, 'Yes')])
    oldpeak = forms.FloatField(label='Oldpeak')
    st_slope = forms.ChoiceField(label='the slope of the peak exercise ST segment', choices=[(1, 'Upsloping'), (2, 'Flat'), (3, 'Downsloping')])


class DoctorVerificationForm(forms.Form):
    result = forms.ChoiceField(
        label='Rezultat medical',
        choices=Prediction.TARGET_CHOICES,
        widget=forms.RadioSelect
    )

    diagnosis = forms.CharField(max_length=255, label='Diagnostic', required=False)
