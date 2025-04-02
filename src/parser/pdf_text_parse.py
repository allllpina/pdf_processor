import os
import PyPDF2

class PdfParseText:
    @staticmethod
    def parse_text_pdf(file_path, output_path):
        try:
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                with open(f'{output_path}/{file_name}.txt', 'w', encoding='utf-8') as txt_file:
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            txt_file.write(text + '\n')
                return {"message": f"File {file_name}.pdf successfully parsed!"}

        except Exception as e:
            # Обробка помилок при записі у файл
            return {"error": f"Error writing to file: {e}"}