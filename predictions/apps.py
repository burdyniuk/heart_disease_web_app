from django.apps import AppConfig
import quadratic_svm_prediction_model as prediction_model
import atexit


class PredictionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'predictions'
    predictor = None

    def ready(self):
        self.predictor = prediction_model.initialize()
        atexit.register(self.predictor.terminate)
