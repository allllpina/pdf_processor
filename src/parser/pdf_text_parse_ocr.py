import json
from pdf2image import convert_from_path
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

class PDF_parse_text_OCR:
    def __init__(self, output_json_file):
        self.output_json_file = output_json_file

    def preprocess_image(self, image):
        """Метод, що виконує обробку зображень(сторінок PDF-файлу) для легшого розпізнавання OCR моделлю"""
        # Збільшуємо контрастність
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)  # Збільшення контрастності (можна змінювати значення)

        # Перетворюємо зображення в чорно-біле (binarization)
        image = image.convert('L')  # Перетворюємо в відтінки сірого
        image = image.point(lambda p: p > 128 and 255)  # Бінаризація

        # Застосовуємо фільтр для підвищення гостроти
        image = image.filter(ImageFilter.SHARPEN)
        
        return image

    def extract_text_from_pdf(self, pdf_path, lang = 'ukr'):
        """Метод що витягує текст із PDF-файлу"""
        # Конвертуємо PDF в зображення
        images = convert_from_path(pdf_path)
        
        # Словник для збереження тексту з вказівкою номера сторінки
        pdf_text = {}
        
        # Для кожної сторінки конвертованої в зображення
        for page_num, image in enumerate(images, 1):
            # Попередня обробка зображення
            image = self.preprocess_image(image)
            
            # Використовуємо Tesseract для витягання тексту з українською мовою
            text = pytesseract.image_to_string(image, lang=lang)  # Вказуємо тільки українську мову
            pdf_text[page_num] = text.strip()  # Записуємо текст у словник із номером сторінки
        
        return pdf_text

    def save_text_as_json(self, pdf_text, output_file, encoding='utf-8'):
        """Метод що зберігає текст у файл формату .json"""
        # Записуємо результат у JSON файл
        with open(output_file, 'w', encoding=encoding) as f:
            json.dump(pdf_text, f, ensure_ascii=False, indent=4)

    def scan_text(self, pdf_path):
        """Метод що компонує витягування тексту і зберігання тексту до файлу"""
        extracted_text = self.extract_text_from_pdf(pdf_path)
        self.save_text_as_json(extracted_text, self.output_json_file)

# Приклад роботи

# pdf_path = './src/materials/pdf/test.pdf'
# output_json_file = './src/materials/txt/test.json'

# scaner = PDF_parse_text_OCR(output_json_file=output_json_file)
# scaner.scan_text(pdf_path=pdf_path)

# print(f"Текст успішно збережений у файл {output_json_file}")

