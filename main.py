import json
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import download_file, process_document
from extractor import analyze_page

app = FastAPI()

# --- Request Model ---
class ExtractionRequest(BaseModel):
    document: str

# --- API Endpoint ---
@app.post("/extract-bill-data")
async def extract_bill_data(request: ExtractionRequest):
    temp_file_path = None
    
    # Initialize Response Containers
    all_pages_data = []
    total_tokens_used = {"input": 0, "output": 0}
    total_items_count = 0

    try:
        # 1. Download File
        print(f"Downloading: {request.document}")
        temp_file_path = download_file(request.document)

        # 2. Convert to Images
        print("Processing document...")
        images = process_document(temp_file_path)

        # 3. Iterate through pages and extract data
        for i, img in enumerate(images):
            page_num = i + 1
            print(f"Analyzing Page {page_num}...")
            
            # Call AI
            json_text, in_tok, out_tok = analyze_page(img, page_num)
            
            # Parse JSON
            page_data = json.loads(json_text)
            
            # Fix page number in response to match iteration
            page_data["page_no"] = str(page_num)
            
            # Update Counters
            total_tokens_used["input"] += in_tok
            total_tokens_used["output"] += out_tok
            
            # Count items for this page
            items_on_page = len(page_data.get("bill_items", []))
            total_items_count += items_on_page
            
            all_pages_data.append(page_data)

        # 4. Construct Final Response
        response = {
            "is_success": True,
            "token_usage": {
                "total_tokens": total_tokens_used["input"] + total_tokens_used["output"],
                "input_tokens": total_tokens_used["input"],
                "output_tokens": total_tokens_used["output"]
            },
            "data": {
                "pagewise_line_items": all_pages_data,
                "total_item_count": total_items_count
            }
        }
        
        return response

    except Exception as e:
        print(f"Error: {str(e)}")
        # In case of failure, return 500 but try to follow schema if possible
        return {
            "is_success": False,
            "error": str(e),
            "data": None
        }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)