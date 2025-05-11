import quadratic_svm_prediction_model as prediction_model
import quadratic_svm_prediction_with_probability as prediction_model_with_probability
import matlab

# predictor = prediction_model.initialize()
pred_prob = prediction_model_with_probability.initialize()

input_data = matlab.double([[44, 1, 4, 150, 412, 0, 0, 170, 0, 0.0, 1]])
# {'STSlope'}    {'age'}    {'chestPainType'}    {'cholesterol'}    {'exerciseAngina'} {'fastingBloodSugar'}    {'maxHeartRate'}    {'oldpeak'}    {'restingBpS'}    {'restingEcg'} {'sex'}
# input_data = matlab.double([[2, 57, 2, 236, 0, 0, 174, 0, 130, 2, 0]])

# result = predictor.quadratic_svm_prediction_model(input_data)
result, confidence = pred_prob.quadratic_svm_prediction_with_probability(input_data, nargout=2)

print("Predicție:", result)
print('Confidență:', confidence)

# Închide componenta după utilizare
# predictor.terminate()
pred_prob.terminate()
