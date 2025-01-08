from django.db import models
from django.contrib.auth.models import User


class Prediction(models.Model):
    age = models.IntegerField()
    sex = models.IntegerField()
    chest_pain_type = models.IntegerField()
    resting_bp_s = models.IntegerField()
    cholesterol = models.IntegerField()
    fasting_blood_sugar = models.IntegerField()
    resting_ecg = models.IntegerField()
    max_heart_rate = models.IntegerField()
    exercise_angina = models.IntegerField()
    oldpeak = models.FloatField()
    st_slope = models.IntegerField()
    target = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
