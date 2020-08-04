import json

from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import IntegerField, SelectField, StringField
from wtforms.validators import DataRequired

import urllib.request
import json

class ClientDataForm(FlaskForm):

    SpecialDay = StringField("SpecialDay (int)", validators=[DataRequired()])
    Month = StringField("Month (str like Feb)", validators=[DataRequired()])
    OperatingSystems =StringField("OperatingSystems (int)", validators=[DataRequired()])
    Browser =StringField("Browser (int)", validators=[DataRequired()])
    Region =StringField("Region (int)", validators=[DataRequired()])
    TrafficType =StringField("TrafficType (int)", validators=[DataRequired()])
    VisitorType =StringField("VisitorType (str)", validators=[DataRequired()])
    Weekend =StringField("Weekend (bool True/False)", validators=[DataRequired()])
    Administrative =StringField("Administrative (int)", validators=[DataRequired()])
    Administrative_Duration =StringField("Administrative_Duration (float)", validators=[DataRequired()])
    Informational =StringField("Informational (int) ", validators=[DataRequired()])
    Informational_Duration =StringField("Informational_Duration (float)", validators=[DataRequired()])
    ProductRelated =StringField("ProductRelated (int)", validators=[DataRequired()])
    ProductRelated_Duration =StringField("ProductRelated_Duration (float)", validators=[DataRequired()])
    BounceRates =StringField("BounceRates (float)", validators=[DataRequired()])
    ExitRates =StringField("ExitRates (float)", validators=[DataRequired()])
    PageValues = StringField("PageValues (float)", validators=[DataRequired()])



app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)

def get_prediction(Administrative, Administrative_Duration, Informational, Informational_Duration,
                   ProductRelated, ProductRelated_Duration, BounceRates, ExitRates,PageValues,
                   SpecialDay, Month, OperatingSystems, Browser, Region, TrafficType,
                   VisitorType, Weekend):
    ll = [Administrative, Administrative_Duration, Informational, Informational_Duration,
                   ProductRelated, ProductRelated_Duration, BounceRates, ExitRates,PageValues,
                   SpecialDay, Month, OperatingSystems, Browser, Region, TrafficType,
                   VisitorType, Weekend]
    print(ll)
    # body = {"Administrative": Administrative,
    #         "Administrative_Duration": Administrative_Duration,
    #         "Informational": Informational,
    #         "Informational_Duration":Informational_Duration,
    #         "ProductRelated":ProductRelated,
    #         "ProductRelated_Duration":ProductRelated_Duration,
    #         "BounceRates":BounceRates,
    #         "ExitRates":ExitRates,
    #         "PageValues":PageValues,
    #         "SpecialDay":SpecialDay,
    #         "Month":Month,
    #         "OperatingSystems":OperatingSystems,
    #         "Browser":Browser,
    #         "Region":Region,
    #         'TrafficType':TrafficType,
    #         "VisitorType":VisitorType,
    #         "Weekend":Weekend}

    body = {"SpecialDay": 5, "Month": "May", "OperatingSystems": 3, "Browser": 2,
     "Region": 3, "TrafficType": 4, "VisitorType": "Returning_Visitor",
     "Weekend": False, "Administrative": 5, "Administrative_Duration": 119,
     "Informational": 4, "Informational_Duration": 380, "ProductRelated": 4,
     "ProductRelated_Duration": 188, "BounceRates": 0.000, "ExitRates": 0.006667,
     "PageValues": 0.000000}

    myurl = "http://localhost:5000/api/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    #print (jsondataasbytes)
    response = urllib.request.urlopen(req, jsondataasbytes)
    return json.loads(response.read())

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response)
    print(response)
    return render_template('predicted.html', response=response)


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        data["Administrative"] = request.form.get("Administrative")
        data["Administrative_Duration"] = request.form.get("Administrative_Duration")
        data["Informational"] = request.form.get("Informational")
        data["Informational_Duration"] = request.form.get("Informational_Duration")
        data["ProductRelated"] = request.form.get("ProductRelated")
        data["ProductRelated_Duration"] = request.form.get("ProductRelated_Duration")
        data["BounceRates"] = request.form.get("BounceRates")
        data["ExitRates"] = request.form.get("ExitRates")
        data["PageValues"] = request.form.get("PageValues")
        data["SpecialDay"] = request.form.get("SpecialDay")
        data["Month"] = request.form.get("Month")
        data["OperatingSystems"] = request.form.get("OperatingSystems")
        data["Browser"] = request.form.get("Browser")
        data["Region"] = request.form.get("Region")
        data["TrafficType"] = request.form.get("TrafficType")
        data["VisitorType"] = request.form.get("VisitorType")
        data["Weekend"] = request.form.get("Weekend")

        try:
            response = str(get_prediction(
                data["Administrative"],
                data["Administrative_Duration"],
                data["Informational"],
                data["Informational_Duration"],
                data["ProductRelated"],
                data["ProductRelated_Duration"],
                data["BounceRates"],
                data["ExitRates"],
                data["PageValues"],
                data["SpecialDay"],
                data["Month"],
                data["OperatingSystems"],
                data["Browser"],
                data["Region"],
                data["TrafficType"],
                data["VisitorType"],
                data["Weekend"]
            ))
            print(response)

        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for('predicted', response=response))
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)