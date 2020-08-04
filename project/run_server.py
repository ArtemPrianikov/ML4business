# USAGE
# Start the server:
# 	python run_front_server.py
# Submit a request via Python:
#	python simple_request.py

# import the necessary packages
import dill
import pandas as pd
import os
dill._dill._reverse_typemap['ClassType'] = type
#import cloudpickle
import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime

# initialize our Flask application and the model
app = flask.Flask(__name__)
model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def load_model(model_path):
	# load the pre-trained model
	global model
	with open(model_path, 'rb') as f:
		model = dill.load(f)

modelpath = "./models/model_trained_clf.dill"
load_model(modelpath)

x_train = pd.read_csv('x_train.csv', sep=';')
y_train = pd.read_csv('y_train.csv', sep=';')
model.fit(x_train, y_train.values.ravel())

@app.route("/", methods=["GET"])
def general():
	return """Welcome to revenue shopping prediction process. Please use 'http://<address>/predict' to POST"""

@app.route("/api/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view
	data = {"success": False}
	dt = strftime("[%Y-%b-%d %H:%M:%S]")
	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":

		SpecialDay = ""
		Month = ""
		OperatingSystems =''
		Browser = ''
		Region = ''
		TrafficType = ''
		VisitorType = ''
		Weekend =''
		Administrative =''
		Administrative_Duration=''
		Informational=''
		Informational_Duration=''
		ProductRelated=''
		ProductRelated_Duration=''
		BounceRates=''
		ExitRates=''
		PageValues=''

		request_json = flask.request.get_json()

		SpecialDay = request_json['SpecialDay']
		Month = request_json['Month']
		OperatingSystems = request_json['OperatingSystems']
		Browser = request_json['Browser']
		Region = request_json['Region']
		TrafficType = request_json['TrafficType']
		VisitorType = request_json['VisitorType']
		Weekend = request_json['Weekend']
		Administrative = request_json['Administrative']
		Administrative_Duration = request_json['Administrative_Duration']
		Informational = request_json['Informational']
		Informational_Duration = request_json['Informational_Duration']
		ProductRelated = request_json['ProductRelated']
		ProductRelated_Duration = request_json['ProductRelated_Duration']
		BounceRates = request_json['BounceRates']
		ExitRates = request_json['ExitRates']
		PageValues = request_json['PageValues']

		logger.info(f'{dt} Data: Administrative={Administrative}, Administrative_Duration={Administrative_Duration},'
					f'Informational={Informational}, Informational_Duration={Informational_Duration},'
					f'ProductRelated={ProductRelated}, ProductRelated_Duration={ProductRelated_Duration},'
					f'BounceRates={BounceRates}, ExitRates={ExitRates}, PageValues={PageValues},'
					f'SpecialDay={SpecialDay}, Month={Month}, OperatingSystems={OperatingSystems},'
					f'Browser={Browser}, Region={Region}, TrafficType={TrafficType}, VisitorType={VisitorType},'
					f'Weekend={Weekend}')

		df = pd.DataFrame([{"Administrative": Administrative,
							"Administrative_Duration": Administrative_Duration,
							"Informational": Informational,
							"Informational_Duration":Informational_Duration,
							"ProductRelated":ProductRelated,
							"ProductRelated_Duration":ProductRelated_Duration,
							"BounceRates":BounceRates,
							"ExitRates":ExitRates,
							"PageValues":PageValues,
							"SpecialDay":SpecialDay,
							"Month":Month,
							"OperatingSystems":OperatingSystems,
							"Browser":Browser,
							"Region":Region,
							'TrafficType':TrafficType,
							"VisitorType":VisitorType,
							"Weekend":Weekend}])

		try:
			preds1 = model.predict_proba(df)
			preds2 = model.predict(df)
			p1 = preds1.tolist()
			p2 = preds2.tolist()

			data["predict_ok"] = True
			pass

		except AttributeError as e:
			pass
			logger.warning(f'{dt} Exception: {str(e)}')
			data["predictions"] = str(e)
			data["success"] = False
			return flask.jsonify(data)
	#
	data["predict_proba"] = p1[0][1]
	data["predict_label"] = p2[0]
	# indicate that the request was a success
	data["success"] = True

	# return the data dictionary as a JSON response
	return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading the model and Flask starting server..."
		"please wait until server has fully started"))
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', debug=True, port=port)
