from fastapi import FastAPI
import uvicorn
from files.task_2 import *
# Создание экземпляра FastAPI

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
