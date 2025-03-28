# Instructions

## DOCKER

### DOCKER IMAGE CREATION
```
docker build -t pdf_parser .
```

### DOCKER CONTAINER RUN
```
docker run -it --name pdf_prsr --restart unless-stopped -p 8080:8080 pdf_parser
```

### DOCKER IMAGE STARTING
```
docker start -i pdf_prsr
```

## REQUESTS

### /upload (POST)
#### Body (multipart/form-data)
__file__ - The PDF file to be uploaded

#### Response
```
{
  "filename": "file_name.pdf",
  "message": "File successfully uploaded!"
}
```

### /process_file (POST)
#### Body
__file_name__ - Name of the file to process
```
{
  "filename": "example.pdf",
}
```
#### Response
```
{
  "message": "File example.pdf successfully parsed!"
}
```

### /export_text (GET)
#### Parameters
__file_name__ - Name of the file to retrieve

#### Response
```
{
  "filename": "example.txt",
  "text": "File context here..."
}
```

### /export_file (GET)
#### Parameters
__file_name__ - Name of the file to download

#### Response
- Returns the requested text file for download

### /get_content (GET)
#### Parameters
Empty

#### Response
```
{
  "pdf": [
    "example.pdf"
  ],
  "txt": [
    "example.txt"
  ]
}
```

### /create_pdf_from_text (POST)
__filename__ - назва для новоствореного файлу

__title str__ - заголовок для файлу

__font_size__ - розмір шрифту,

__text_lines__ - масив із рядками тексту, що мають бути записані до файлу

```
{
    filename: Optional[str]: "test.pdf"
    title: Optional[str] = "test"
    font_size: Optional[int] = 15
    text_lines: list[str] = ['test1', 'test2', 'test3']
}
```

#### Response
- Returns the PDF-file for download