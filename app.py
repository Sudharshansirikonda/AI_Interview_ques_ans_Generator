from fastapi import FastAPI, Form,  Request, Response, File, Depends, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
import uvicorn
import os
import aiofiles
import json
import csv
from src.helper import llm_pipeline

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def chat(request: Request, file: bytes = File(...)):
    file_path = "uploaded_file.pdf"
    
    async with aiofiles.open(file_path, 'wb') as out_file:
        await out_file.write(file)

    try:
        result = llm_pipeline(file_path)
        response_data = {
            "status": "success",
            "data": result
        }
    except Exception as e:
        response_data = {
            "status": "error",
            "message": str(e)
        }
    
    return templates.TemplateResponse("result.html", {"request": request, "response_data": jsonable_encoder(response_data)})

def get_csv(file_path):
    answer_generation_chain, ques_list = llm_pipeline(file_path)
    base_folder = "static/csv_files"
    os.makedirs(base_folder, exist_ok=True)
    csv_file_path = os.path.join(base_folder, "output.csv")
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Question", "Answer"])
        for question in ques_list:
            answer = answer_generation_chain.run(question)
            writer.writerow([question, answer])
    return csv_file_path

@app.get("/download_csv")
async def download_csv(request: Request):
    csv_file_path = get_csv("uploaded_file.pdf")
    return templates.TemplateResponse("download.html", {"request": request, "csv_file_path": csv_file_path})
@app.get("/download")
async def download_file(request: Request):
    csv_file_path = "static/csv_files/output.csv"
    if os.path.exists(csv_file_path):
        return templates.TemplateResponse("download.html", {"request": request, "csv_file_path": csv_file_path})
    else:
        return templates.TemplateResponse("error.html", {"request": request, "message": "File not found."})
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    

    