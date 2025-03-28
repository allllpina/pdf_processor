from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from datetime import datetime
import os

class PDF_composer:
    def __init__(self, save_path: str):
        """save_path: str - шлях, за яким мають зберігатись всі новостворені PDF-файли"""
        self.save_path = save_path

    def generate_pdf(
        self,
        filename: str = None,
        title: str = None,
        font_size: int = None,
        text_lines: list[str] = None
    ):
        """Функція, що перетворює масив із рядками тексту у повноцінний PDF-файл.
        filename: str - назва для новоствореного файлу
        title: str - заголовок для файлу
        font_size: int - розмір шрифту,
        text_lines: list[str] - масив із рядками тексту, що мають бути записані до файлу"""
        try:
            if text_lines is None or not isinstance(text_lines, list):
                raise ValueError("Text lines must be a non-empty list of strings")
            
            # Встановлюємо назву файлу за замовчуванням
            if filename is None:
                filename = datetime.now().strftime("%d%m%Y-%H-%M") + ".pdf"
            
            # Встановлюємо розмір шрифту за замовчуванням
            if font_size is None:
                font_size = 10  # Трохи менший за середній, але читабельний
            
            # Формуємо повний шлях до файлу
            file_path = os.path.join(self.save_path, filename)
            
            # Перевіряємо, чи існує директорія, і створюємо її за необхідності
            os.makedirs(self.save_path, exist_ok=True)
            
            # Створення PDF-файлу
            pdf = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter
            max_width = width - 100  # Враховуємо поля
            
            # Додаємо заголовок, якщо він є
            y_position = height - 50  # Відступ зверху
            if title:
                pdf.setFont("Helvetica-Bold", font_size + 2)
                pdf.drawString(50, y_position, title)
                y_position -= 20  # Відступ після заголовка
            
            # Додаємо текст з автоматичним перенесенням рядків
            pdf.setFont("Helvetica", font_size)
            for line in text_lines:
                wrapped_lines = simpleSplit(line, "Helvetica", font_size, max_width)
                for wrapped_line in wrapped_lines:
                    if y_position < 50:  # Перевіряємо, чи є місце на сторінці
                        pdf.showPage()
                        pdf.setFont("Helvetica", font_size)
                        y_position = height - 50
                    pdf.drawString(50, y_position, wrapped_line)
                    y_position -= 15
            
            pdf.save()
            print(f"PDF '{file_path}' successfully created.")
            return file_path
        
        except Exception as e:
            return {'error': f"Error creating PDF: {e}"}

