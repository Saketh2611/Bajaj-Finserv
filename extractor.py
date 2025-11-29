import os
import typing_extensions
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Literal
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- Define the Output Schema (Pydantic) ---
class BillItem(BaseModel):
    item_name: str = Field(description="Name of the service or medicine exactly as in the bill")
    item_amount: float = Field(description="Net amount of the item post discounts")
    item_rate: float = Field(description="Unit rate of the item")
    item_quantity: float = Field(description="Quantity of the item. Default to 1.0 if not specified")

class PageData(BaseModel):
    page_no: str = Field(description="The page number formatted as string")
    page_type: Literal["Bill Detail", "Final Bill", "Pharmacy"] = Field(description="Type of the page")
    bill_items: List[BillItem] = Field(description="List of line items found on this page")

# --- The AI Extraction Logic ---
def analyze_page(image, page_number):
    """
    Sends a single page image to Gemini Flash and returns structured JSON.
    """
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = """
    You are an expert medical data extractor. Analyze this medical bill page.
    
    1. **Identify Page Type**: 
       - 'Pharmacy': Lists medicines with distinct batches/expiry/discounts.
       - 'Bill Detail': Lists hospital services, consultations, room charges.
       - 'Final Bill': A summary page showing total amounts or consolidated categories.
    
    2. **Extract Line Items**:
       - Extract every chargeable line item (Name, Rate, Qty, Amount).
       - **CRITICAL RULE**: Do NOT extract 'Subtotal', 'Grand Total', 'Total', or 'Net Payable' rows as line items. We will calculate the total ourselves.
       - If a column is missing (e.g., Quantity), infer reasonable defaults (e.g., 1.0).
       - Ensure all amounts are floats (e.g., 1500.00).

    3. **Double Counting Prevention**:
       - If this is a 'Final Bill' page that only summarizes items listed on previous pages, return an EMPTY list for bill_items to avoid double counting. 
       - Only list items on a 'Final Bill' page if they are NEW charges not shown previously.
    """

    try:
        # Structured generation ensures we get exact JSON format
        result = model.generate_content(
            [image, prompt],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=PageData
            )
        )
        
        # Calculate token usage manually if needed, or extract from metadata
        usage = result.usage_metadata
        input_tok = usage.prompt_token_count
        output_tok = usage.candidates_token_count
        
        return result.text, input_tok, output_tok

    except Exception as e:
        print(f"AI Error on page {page_number}: {e}")
        # Return empty safe fallback
        return '{"page_no": "'+str(page_number)+'", "page_type": "Bill Detail", "bill_items": []}', 0, 0