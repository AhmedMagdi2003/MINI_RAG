from fastapi import FastAPI
app = FastAPI()
@app.get("/welcom")
def welcom():
    return {'message':'Hello world'}