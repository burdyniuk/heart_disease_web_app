from django.db import models
from django.contrib.auth.models import User


class Prediction(models.Model):
    SEX_CHOICES = [
        (0, 'Female'),
        (1, 'Male'),
    ]
    CHEST_PAIN_CHOICES = [
        (1, 'Typical Angina'),
        (2, 'Atypical Angina'),
        (3, 'Non-anginal Pain'),
        (4, 'Asymptomatic'),
    ]
    FASTING_BLOOD_SUGAR_CHOICES = [
        (0, 'False'),
        (1, 'True'),
    ]
    RESTING_ECG_CHOICES = [
        (0, 'Normal'),
        (1, 'having ST-T wave abnormality'),
        (2, "showing probable or definite left ventricular hypertrophy by Estes' criteria"),
    ]
    EXERCISE_ANGINA_CHOICES = [
        (0, 'No'),
        (1, 'Yes'),
    ]
    ST_SLOPE_CHOICES = [
        (1, 'Upsloping'),
        (2, 'Flat'),
        (3, 'Downsloping'),
    ]

    TARGET_CHOICES = [
        (0, 'False'),
        (1, 'True'),
    ]

    age = models.IntegerField()
    sex = models.IntegerField(choices=SEX_CHOICES)
    chest_pain_type = models.IntegerField(choices=CHEST_PAIN_CHOICES)
    resting_bp_s = models.IntegerField()
    cholesterol = models.IntegerField()
    fasting_blood_sugar = models.IntegerField(choices=FASTING_BLOOD_SUGAR_CHOICES)
    resting_ecg = models.IntegerField(choices=RESTING_ECG_CHOICES)
    max_heart_rate = models.IntegerField()
    exercise_angina = models.IntegerField(choices=EXERCISE_ANGINA_CHOICES)
    oldpeak = models.FloatField()
    st_slope = models.IntegerField(choices=ST_SLOPE_CHOICES)
    target = models.IntegerField(choices=TARGET_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Prediction {self.id}'
