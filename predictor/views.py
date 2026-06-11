import os
import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.conf import settings
import pandas as pd
from .prediction import charts_f
base_path=os.path.join(settings.BASE_DIR,"models")
# Load .pkl files
featurePath = os.path.join(settings.BASE_DIR, "cricket","models","selected_features1.pkl")
features = joblib.load(featurePath)

modelPath = os.path.join(settings.BASE_DIR, "cricket","models","randomforest_model.pkl")
model = joblib.load(modelPath)

scalerPath=os.path.join(settings.BASE_DIR,"cricket","models","scaler.pkl")
scaler=joblib.load(scalerPath)
norm_col=['Runs to Get','Balls Remaining','Required run rate','Current run rate','Pressure','Momentum','Wickets Left','Bat_First_Rating','Bat_Second_Rating','Bowler Economy']
model_features=model.feature_names_in_
# Home page
def Home(request):
    return render(request, 'cricket/home.html')
# Prediction page
def prediction(request):
    if request.method == "POST":
        file = request.FILES.get('json_file')  # match your form field name
        if file:
            try:
              upload_dir=os.path.join(settings.BASE_DIR,"uploads")
              os.makedirs(upload_dir,exist_ok=True)
              temp_json_path=os.path.join(upload_dir,file.name)
              with open(temp_json_path,'wb+') as destination:
                for chunk in file.chunks():
                   destination.write(chunk)
              match_id,charts_data=charts_f(temp_json_path)
              return render(request, 'cricket/result.html',{"match_id":match_id,"charts":charts_data})
            except Exception as e:
                print("ERROR IN CHARTS:", e)  
                return render(request, 'cricket/result.html', {
                    "error": f"Prediction failed: {str(e)}"
                })
    # Always return something for GET or missing file
    return render(request, 'cricket/prediction.html')
          
