from fastapi import FastAPI, HTTPException, Form
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(
    supabase_url=os.getenv("SUPABASE_URL"),
    supabase_key=os.getenv("SUPABASE_KEY")
)

app = FastAPI()

# Configure CORS for local development only
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js development server
    allow_credentials=True,
    allow_methods=["POST"],  # Only allow POST requests
    allow_headers=["*"],
)

@app.post('/verify')

def verify(email: str = Form(...), name: str = Form(...)):
    #get domain
    domain = email.split('@')[-1]
    #check database
    try:
        # Query the 'school_data' table in Supabase database
        # - Select only the 'website' column
        # - Filter where the 'domain' column equals the email domain
        # - Execute the query and return the result
        result = supabase.table('school_data').select('website').eq('domain', domain).execute()
        print(result)
        if not result.data:
            raise HTTPException(status_code=404, detail='School not found')
        
        website = result.data[0]['website']
        #TODO more fullproof method of getting webiste (not all are .com)
        #TODO add other sports not just mens soccer
        roster = website + '/sports/mens-soccer/roster'

        #get the roster
        #TODO fix check for wrong page loaded
        try:
            page = requests.get(roster)
            soup = BeautifulSoup(page.text, 'html.parser')
        except Exception:
            raise HTTPException(status_code=500, detail='Failed to fetch roster')
        
        #TODO find better method
        if name.lower() in soup.get_text().lower():
            return {"status": "valid"}
        else:
            return {"status": "invalid"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

