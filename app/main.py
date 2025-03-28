import os
import shutil
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from parser.pdf_text_parse import PdfParseText
from request_models import ParseText

# Завантаження змінних середовища для конфігурації
UPLOAD_DIR = os.getenv("UPLOAD_DIR", './materials/pdf')
RESULT_DIR = os.getenv("RESULT_DIR", "./materials/txt")

# Ініціалізація FastAPI додатку
app = FastAPI()

try:
    # Створення об'єкта для парсингу pdf
    prs = PdfParseText()
except Exception as e:
    # Обробка помилок при ініціалізації
    raise RuntimeError({"error": f"Error initialisation service: {str(e)}"})

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        if not file.file:
            result = {"error": "No file uploaded!"}
        else:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            result = {"filename": file.filename, "message": "File successfully uploaded!"}
        return result
    except Exception as e:
        # Обробка помилок при завантаженні файлу
        raise HTTPException(status_code=500, detail={"error": f"Error while scanning text: {str(e)}"})

@app.post("/process_file")
async def process_file(request: ParseText):
    try:
        # Перевірка існування файлу
        if request.file_name and not os.path.exists(f'{UPLOAD_DIR}/{request.file_name}'):
            return {"error": f"File '{request.file_name}' does not exist!"}

        # Парсинг файлу
        result = prs.parse_text_pdf(f'{UPLOAD_DIR}/{request.file_name}')

        print(result)  # Виведення результату в консоль для налагодження
        return result  # Повернення результату клієнту
    except Exception as e:
        # Обробка помилок при скануванні тексту
        raise HTTPException(status_code=500, detail={"error": f"Error while scanning text: {str(e)}"})

@app.get("/export_text")
async def export_text(file_name: str):
    try:
        # Перевірка існування файлу
        if file_name and not os.path.exists(f'{RESULT_DIR}/{file_name}'):
            return {"error": f"File '{file_name}' does not exist!"}

        with open(f'{RESULT_DIR}/{file_name}', "r", encoding="utf-8") as file:
            file_content = file.read()

        result = {"filename": file_name, "text": file_content}

        print(result)  # Виведення результату в консоль для налагодження
        return result  # Повернення результату клієнту
    except Exception as e:
        # Обробка помилок при скануванні тексту
        raise HTTPException(status_code=500, detail={"error": f"Error while scanning text: {str(e)}"})

@app.get("/export_file")
async def export_file(file_name: str):
    try:
        # Перевірка існування файлу
        if file_name and not os.path.exists(f'{RESULT_DIR}/{file_name}'):
            return {"error": f"File '{file_name}' does not exist!"}

        result = FileResponse(f'{RESULT_DIR}/{file_name}', media_type="text/plain", filename="result.txt")

        print(result)  # Виведення результату в консоль для налагодження
        return result  # Повернення результату клієнту
    except Exception as e:
        # Обробка помилок при скануванні тексту
        raise HTTPException(status_code=500, detail={"error": f"Error while scanning text: {str(e)}"})

@app.get("/get_content")
async def get_content():
    try:
        # Викликається метод виводу всіх файлів
        result = {"pdf": os.listdir(UPLOAD_DIR), "txt": os.listdir(RESULT_DIR)}
        print(result)  # Виведення результату в консоль для налагодження
        return result  # Повернення результату клієнту
    except Exception as e:
        # Обробка помилок при виводі всіх слів
        raise HTTPException(status_code=500, detail={"error": f"Error while listing databases: {str(e)}"})