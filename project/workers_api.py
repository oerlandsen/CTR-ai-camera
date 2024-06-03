from fastapi import FastAPI, UploadFile
from workers_broker_app  import process_frame


app = FastAPI()

@app.get("/heartbeat")
def read_root():
    return {"status": True}

@app.post("/camera/{camera_id}/frame/{frame_id}")
def post_process_frame(camera_id: int, frame_id: int, frame: UploadFile):
    job = process_frame.delay(frame_id, frame.file.read(), camera_id)
    return {
        "message": "process_frame job published",
        "job_id": job.id,
    }

@app.get("/add/{job_id}")
def get_job(job_id: str):
    job = process_frame.AsyncResult(job_id)
    return {
        "ready": job.ready(),
        "result": job.result,
    }
