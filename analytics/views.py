from django.shortcuts import render
from predictions.models import Prediction
from django.db.models import Count


def analytics_view(request):
	all_predictions = Prediction.objects.all().count()
	validated_count = Prediction.objects.filter(medical_result__isnull=False).count()

	target_counts = (
		Prediction.objects.values('target')
		.annotate(count=Count('target'))
		.order_by('target')
	)

	charts = {
		'target_repartition': {
			'labels': [("Risc" if entry['target'] else "Fără risc") for entry in target_counts],
			'values': [entry['count'] for entry in target_counts],
		}
	}

	sex_disease_counts = (
		Prediction.objects.filter(target=1).values('sex')
		.annotate(count=Count('sex'))
		.order_by('sex')
	)

	charts['sex_repartition'] = {
		'labels': [("Barbati" if entry['sex'] else "Femei") for entry in sex_disease_counts],
		'values': [entry['count'] for entry in sex_disease_counts],
		'total_males': Prediction.objects.filter(sex=1).count(),
		'total_females': Prediction.objects.filter(sex=0).count()
	}

	diagnosis_counts = (
		Prediction.objects.filter(medical_result=1).values('diagnosis')
		.annotate(count=Count('diagnosis'))
		.order_by('diagnosis')
	)

	charts['diagnosis_repartition'] = {
		'labels': [entry['diagnosis'] for entry in diagnosis_counts],
		'values': [entry['count'] for entry in diagnosis_counts]
	}

	ages_repartition = (
		Prediction.objects.filter(medical_result=1).values("age")
		.annotate(count=Count("id"))
		.order_by("age")
	)

	charts['ages_repartition'] = {
		'labels': [entry['age'] for entry in ages_repartition],
		'values': [entry['count'] for entry in ages_repartition]
	}

	return render(request, 'analytics/analytics.html', {
		'charts': charts,
		'all_predictions': all_predictions,
		'validated_count': validated_count,
	})

