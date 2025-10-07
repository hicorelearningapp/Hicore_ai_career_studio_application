import os, shutil, time
from fastapi import UploadFile
from typing import Optional

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_file(file: Optional[UploadFile]) -> Optional[str]:
    if not file:
        return None
    filename = f"{int(time.time())}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return path

def model_to_dict(model):
    return {k: v for k, v in model.__dict__.items() if k != "_sa_instance_state"}
