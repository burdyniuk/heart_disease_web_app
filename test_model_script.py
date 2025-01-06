import prediction_model_function as prediction_model
import matlab

predictor = prediction_model.initialize()

input_data = matlab.double([[44, 1, 4, 150, 412, 0, 0, 170, 0, 0.0, 1]])

result = predictor.prediction_model_function(input_data)

print("Predicție:", int(result))

# Închide componenta după utilizare
predictor.terminate()
