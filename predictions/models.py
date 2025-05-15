from django.db import models
from django.contrib.auth.models import User


class Prediction(models.Model):
    SEX_CHOICES = [
        (0, 'Femeie'),
        (1, 'Bărbat'),
    ]
    CHEST_PAIN_CHOICES = [
        (1, 'Angină tipică'),
        (2, 'Angină atipică'),
        (3, 'Durere non-anginală'),
        (4, 'Asimptomatic'),
    ]
    FASTING_BLOOD_SUGAR_CHOICES = [
        (0, 'Sub 120 mg/dl'),
        (1, 'Peste 120 mg/dl'),
    ]
    RESTING_ECG_CHOICES = [
        (0, 'Normal'),
        (1, 'Anomalie undă ST-T'),
        (2, "Prezintă hipertrofie ventriculară stângă probabilă sau certă după criteriile Estes"),
    ]
    EXERCISE_ANGINA_CHOICES = [
        (0, 'Nu'),
        (1, 'Da'),
    ]
    ST_SLOPE_CHOICES = [
        (1, 'Ascendent'),
        (2, 'Plat'),
        (3, 'Descendent'),
    ]

    TARGET_CHOICES = [
        (0, 'Nu există risc'),
        (1, 'Există risc'),
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
    confidence = models.FloatField(null=True, blank=True)  # Optional confidence field
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    medical_result = models.IntegerField(choices=TARGET_CHOICES, null=True, blank=True)
    diagnosis = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'Prediction {self.id}'
