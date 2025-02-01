from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from io import BytesIO

app = FastAPI()

@app.post("/upload-excel/")
async def upload_excel(file: UploadFile = File(...)):
    """
    Endpoint to upload an Excel file, process it, and return a JSON response.
    """
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an Excel file.")
    
    try:
        # Read the Excel file
        content = await file.read()
        excel_data = pd.read_excel(BytesIO(content))

        # Replace NaN and Infinity with None (JSON-compliant)
        json_data = excel_data.replace({float('nan'): None, float('inf'): None, -float('inf'): None}).to_dict(orient="records")
        
        # Return the JSON response
        return JSONResponse(content=json_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
