import os
import requests
import tempfile
from pdf2image import convert_from_path
from PIL import Image

def download_file(url: str) -> str:
    """
    Downloads a file from a URL to a temporary file and returns the file path.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Determine extension from headers or url, default to .pdf
        content_type = response.headers.get('content-type')
        suffix = ".pdf"
        if "image/jpeg" in content_type: suffix = ".jpg"
        elif "image/png" in content_type: suffix = ".png"
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            for chunk in response.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
            return tmp_file.name
    except Exception as e:
        raise Exception(f"Failed to download file: {str(e)}")

def process_document(file_path: str) -> list[Image.Image]:
    """
    Converts a PDF or Image file path into a list of PIL Images.
    """
    images = []
    try:
        if file_path.lower().endswith(".pdf"):
            # Convert PDF to list of images (requires poppler installed)
            images = convert_from_path(file_path)
        else:
            # It's already an image
            img = Image.open(file_path)
            # Ensure it's in RGB mode
            if img.mode != 'RGB':
                img = img.convert('RGB')
            images = [img]
        
        return images
    except Exception as e:
        raise Exception(f"Failed to process document: {str(e)}")
    finally:
        # Clean up the temp file
        if os.path.exists(file_path):
            os.remove(file_path)