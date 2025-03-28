import os
import shutil

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse

from parser.pdf_text_parse import PdfParseText
from composer.pdf_composer import PDF_composer

from request_models import ParseText, CreatePdfFromText

# Завантаження змінних середовища для конфігурації
UPLOAD_DIR = os.getenv("UPLOAD_DIR", './src/materials/pdf')
RESULT_DIR = os.getenv("RESULT_DIR", "./src/materials/txt")
CREATED = os.getenv("CREATED", "./src/materials/created")

# Ініціалізація FastAPI додатку
app = FastAPI()

try:
    # Створення об'єкта для парсингу pdf
    prs = PdfParseText()
    pdf_cmpsr = PDF_composer(f"{CREATED}/")
except Exception as e:
    # Обробка помилок при ініціалізації
    raise RuntimeError({"error": f"Error initialisation service: {str(e)}"})

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API Home</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                flex-direction: column;
            }
            button {
                font-size: 20px;
                padding: 10px 20px;
                background-color: #007BFF;
                color: white;
                border: none;
                cursor: pointer;
                border-radius: 5px;
            }
            button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <h1>PDF processing API</h1>
        <button onclick="window.location.href='/docs'">Test API</button>
    </body>
    </html>
    """

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
    
@app.post("/create_pdf_from_text")
async def create_pdf_from_text(request: CreatePdfFromText):
    try:
        file_path = pdf_cmpsr.generate_pdf(
            filename = request.filename,
            title = request.title,
            font_size = request.font_size,
            text_lines = request.text_lines
                                        )
        if not os.path.exists(file_path):
                raise {"error": f"File '{request.filename}' hasn't been created!"}
        
        result = FileResponse(file_path, media_type="application/pdf",filename= request.filename)

        print(result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail= {'error': f'Error while creating a file: {str(e)}'})
