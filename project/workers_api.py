from fastapi import FastAPI
from workers_broker_app  import add

app = FastAPI()

@app.get("/heartbeat")
def read_root():
    return {"status": True}


# Example of sending a task to the worker and then getting the result

@app.post("/add/{x}/{y}")
def post_publish_job(x : int, y : int):
    job = add.delay(x, y)
    return {
        "message": "add job published",
        "job_id": job.id,
    }

@app.get("/add/{job_id}")
def get_job(job_id: str):
    job = add.AsyncResult(job_id)
    return {
        "ready": job.ready(),
        "result": job.result,
    }
