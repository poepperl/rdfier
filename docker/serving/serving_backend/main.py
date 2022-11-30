import sys
import inspect
import asyncio
import config
import logging

import uvicorn
from fastapi import FastAPI

from logging.handlers import TimedRotatingFileHandler

app = FastAPI()
model = None
logger = None
model_path = "/opt/ml/model"


@app.get("/")
def read_root():
    return "Use the /doc entpoint to see API documentation."

def validate_data(data):
    # check if everything is there
    # check if all values within speck
    # - ranges
    # - categories
    pass

def preprocess_data(data):
    # encoding
    # tranformation
    # can be part of e.g. sklearn pipeline
    return data    

@app.post("/inference")
async def inference(request):
    data = request.json()
    # save data for data drift and model_drift measuremnt
    validate_data(data)
    data = preprocess_data()
    prediction = None #replace with model predict code
    return prediction

@app.get("/model_description")
async def model_description():

    pass


def get_size(obj, seen=None):
    """Recursively finds size of objects
       https://github.com/bosswissam/pysize/blob/master/pysize.py
    """
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if hasattr(obj, '__dict__'):
        for cls in obj.__class__.__mro__:
            if '__dict__' in cls.__dict__:
                d = cls.__dict__['__dict__']
                if inspect.isgetsetdescriptor(d) or inspect.ismemberdescriptor(d):
                    size += get_size(obj.__dict__, seen)
                break
    if isinstance(obj, dict):
        size += sum((get_size(v, seen) for v in obj.values()))
        size += sum((get_size(k, seen) for k in obj.keys()))
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum((get_size(i, seen) for i in obj))
        
    if hasattr(obj, '__slots__'): # can have __slots__ with __dict__
        size += sum(get_size(getattr(obj, s), seen) for s in obj.__slots__ if hasattr(obj, s))
        
    return size


def load_model(model_file):
    logger.info("Start loading model.")
    model = None
    model_size = get_size(model)
    logger.info("Model loaded.")
    logger.info(f"Model using {model_size} Byte of RAM.")
    return model


def create_logger(path, log_mode):
    logger = logging.getLogger()
    logger.setLevel(log_mode)

    handler = TimedRotatingFileHandler(path, when="d", interval=1, backupCount=5)
    logger.addHandler(handler)
    return logger


if __name__ == "__main__":
    log_mode = logging.INFO
    port = 8080
    model_file="model.pkl"

    logger = create_logger("logging.log", log_mode)
    model = load_model(model_file)

    uvicorn.run("main:app", host="0.0.0.0", port=port)
