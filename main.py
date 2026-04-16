from fastapi import FastAPI

# api obejct
app=FastAPI()

#end point 
@app.get("/")  #home page
#function for endpoint 
def hello():
    return {"message":"Hello World"}   

#end point 
@app.get("/welcome") #welcome page
#function for endpoint
def welcome():
    return {"message":"Welcome to Saylani Mass IT Training"}