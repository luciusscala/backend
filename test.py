from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Print environment variables (for debugging)
print("Checking environment variables...")
print(f"SUPABASE_URL exists: {'SUPABASE_URL' in os.environ}")
print(f"SUPABASE_KEY exists: {'SUPABASE_KEY' in os.environ}")

# Initialize Supabase client
try:
    print("\nInitializing Supabase client...")
    supabase: Client = create_client(
        supabase_url=os.getenv("SUPABASE_URL"),
        supabase_key=os.getenv("SUPABASE_KEY")
    )
    print("Supabase client initialized successfully!")
except Exception as e:
    print(f"Error initializing Supabase client: {str(e)}")
    exit(1)

# Get all rows from the school_data table
try:
    print("\nQuerying database...")
    response = supabase.table('school_data').select('*').execute()
    data = response.data
    
    if not data:
        print("No data found in the school_data table")
    else:
        print("\nAll rows in school_data table:")
        print("-" * 50)
        for row in data:
            print(f"Domain: {row.get('domain', 'N/A')}")
            print(f"Website: {row.get('website', 'N/A')}")
            print("-" * 50)
        
        print(f"\nTotal rows: {len(data)}")
    
except Exception as e:
    print(f"Error querying database: {str(e)}")
    print(f"Error type: {type(e).__name__}") 