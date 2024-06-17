
# from workers_broker_app  import process_frame
# import cv2
# import numpy as np

# # checkpoint hay que separar el broker de la api

# app = FastAPI()

# @app.get("/heartbeat")
# def read_root():
#     return {"status": True}

# @app.post("/camera/{camera_id}/frame/{frame_id}")
# def post_process_frame(camera_id: int, frame_id: int, frame: UploadFile):

#     frame_mat = cv2.imdecode(np.frombuffer(frame.file.read(), np.uint8), cv2.IMREAD_COLOR).tolist()
#     job = process_frame.delay(frame_id, frame_mat, camera_id)

#     return {
#         "message": "process_frame job published",
#         "job_id": job.id,
#     }

# @app.get("/post_process_frame/{job_id}")
# def get_job(job_id: str):
#     job = process_frame.AsyncResult(job_id)
#     return {
#         "ready": job.ready(),
#         "result": job.result,
#     }


from fastapi import FastAPI, UploadFile, File, Form
from celery.result import AsyncResult
import os
from celery import Celery
import numpy as np

app = FastAPI()

celery_app = Celery(
    'CTR-cameras',
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
)

@app.post("/camera")
async def new_process(
    frame: UploadFile = File(...),
    camera_id: int = Form(...),
    frame_id: int = Form(...)
  ):
    
    frame_content = await frame.read()
    data = {
        "camera_id": camera_id,
        "frame_id": frame_id,
        "frame_content": frame_content
    }

    task = celery_app.send_task("workers_broker_app.process_frame_task", args=[data])
    return {"task_id": task.id}

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == 'PENDING':
        return {"status": "PENDING"}
    elif task_result.state == 'SUCCESS':
        return {"status": "SUCCESS", "result": task_result.result}
    elif task_result.state == 'FAILURE':
        return {"status": "FAILURE", "error": str(task_result.result)}
    else:
        return {"status": task_result.state}

































