import os
import random

import quadratic_svm_prediction_with_probability as prediction_model_with_probability
import django
import matlab
import pandas as pd
from sklearn.model_selection import train_test_split


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heart_disease_web_app.settings')

django.setup()

from predictions.models import Prediction
from django.contrib.auth.models import User
user = User.objects.get(id=1)

dataset_path = r'C:\Users\burdyniuk\Desktop\master\disertatia\datasets\new_set.csv'
HEART_DISEASES = [
	'Boala coronariana',
	'Accidentul vascular cerebral',
	'Boala cardiaca reumatismala',
	'Boala cardiaca congenitala',
	'Anevrism de aorta / disectie',
	'Tromboza venoasa profunda'
]


train_data = pd.read_csv(dataset_path)
y = train_data['target']
x = train_data.drop(columns=['target'])
pred_prob = prediction_model_with_probability.initialize()

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

for index, row in x_test.iterrows():
	print(row)
	input_data = matlab.double([[row['ST slope'], row['age'], row['chest pain type'], row['cholesterol'], row['exercise angina'], row['fasting blood sugar'], row['max heart rate'], row['oldpeak'], row['resting bp s'], row['resting ecg'], row['sex']]])
	result, confidence = pred_prob.quadratic_svm_prediction_with_probability(input_data, nargout=2)
	print(result, confidence)
	y_value = y_test.loc[index]

	if y_value:
		prediction = Prediction(
			age=row['age'], sex=row['sex'], chest_pain_type=row['chest pain type'],
			resting_bp_s=row['resting bp s'], cholesterol=row['cholesterol'],
			fasting_blood_sugar=row['fasting blood sugar'], resting_ecg=row['resting ecg'],
			max_heart_rate=row['max heart rate'], exercise_angina=row['exercise angina'],
			oldpeak=row['oldpeak'], st_slope=row['ST slope'], target=result, confidence=confidence,
			created_by=user, diagnosis=random.choice(HEART_DISEASES), medical_result=y_value
		)
	else:
		prediction = Prediction(
			age=row['age'], sex=row['sex'], chest_pain_type=row['chest pain type'],
			resting_bp_s=row['resting bp s'], cholesterol=row['cholesterol'],
			fasting_blood_sugar=row['fasting blood sugar'], resting_ecg=row['resting ecg'],
			max_heart_rate=row['max heart rate'], exercise_angina=row['exercise angina'],
			oldpeak=row['oldpeak'], st_slope=row['ST slope'], target=y_value, confidence=confidence,
			created_by=user, medical_result=y_value
		)
	prediction.save()


