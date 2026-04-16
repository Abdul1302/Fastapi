from fastapi import FastAPI, Path, HTTPException, Query
import json


# api obejct
app=FastAPI()


# function returns the  data from json file
def load_data():
    with open("my_petients.json","r") as f:
        data=json.load(f)

    return data



#end point to retrieve data
@app.get("/")  #home page
#function for endpoint 
def hello():
    return {"message":"Patient Management System"}   

#end point retrieve data
@app.get("/about") #about page
#function for endpoint
def about():
    return {"message":"A fully functional api to manage patient records"}


#end point TO retrieve data from json file
@app.get("/view")
#function to view patients data
def view():
    data=load_data()

    return data 

# end point to retrieve data of a particular patient
@app.get("/view/{patient_id}")
#function to view data of a particular patient with path function 
def view_patient(patient_id = Path(..., description="The ID of the patient in the DB",example="P001")):
    #load all patient data from json file
    data=load_data()

    if patient_id in data:
        return data[patient_id]
    else:
        # raising http not found error if petient_id not exist
        raise HTTPException(status_code=404, detail="Patient not Found")

@app.get("/sort")
#function to sort patient data based on height, weight and bmi with query function 
def sort_petient(sort_by=Query(..., description="Sort on the basis of height, weight, bmi and age"),
                 order=Query('asc', description="Sort in ascending or descending order")):
   
    valid_fields = ['height', 'weight', 'bmi', 'age']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field select from {valid_fields}")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order select between 'asc' and 'desc' ")
    
    data=load_data()

    sort_order= True if order == 'desc' else False

    sorted_data=sorted(data.values(),key=lambda x: x.get(sort_by,0), reverse=sort_order)

    return sorted_data
