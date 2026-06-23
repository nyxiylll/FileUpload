import os 
from fastapi import FastAPI , UploadFile , HTTPException , File , status
from supabase import Client , create_client
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase : Client = create_client(SUPABASE_URL,SUPABASE_KEY)

BUCKET_NAME = os.getenv("SUPABASE_BUCKET_NAME")

class Request(BaseModel):
    filename : str

@app.get("/")
def root():
    return {"Message":"Welcome"}

@app.post("/Upload")
async def Upload_file(file_name : Request):
    try:
        unique_id = os.urandom(4).hex()
        file_path = f"uploads/{unique_id}_{file_name.filename}"

        response = supabase.storage.from_(BUCKET_NAME).create_signed_upload_url(file_path)

        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(file_path)

        return {
                "success": True,
                "upload_url" : response["signed_url"],
                "final_asset_url" : public_url
            }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
