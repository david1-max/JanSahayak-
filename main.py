from fastapi import FastAPI

# This creates your actual application
app = FastAPI(title="JanSahayak API")

# This is a "route" - a specific URL endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the JanSahayak Eligibility Engine!"}