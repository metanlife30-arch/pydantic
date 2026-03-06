from fastapi import FastAPI, HTTPException, Path, Query,Depends
from typing import Optional, List, Dict, Annotated
import uvicorn
from files.task_2 import test_validate_call
# Создание экземпляра FastAPI

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
