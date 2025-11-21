import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document
from schemas import Delegate

app = FastAPI(title="Rhetorix MUN API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Rhetorix MUN Backend Running"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the Rhetorix backend API!"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


# Public config for the event
class EventConfig(BaseModel):
    name: str
    date: str
    venue: str
    registration_open: bool
    contact_email: str


@app.get("/api/config", response_model=EventConfig)
def get_config():
    return EventConfig(
        name="Rhetorix Model United Nations",
        date="2025-02-22 to 2025-02-23",
        venue="To be announced",
        registration_open=True,
        contact_email="secretariat@rhetorixmun.org",
    )


# Committees listing
class Committee(BaseModel):
    code: str
    name: str
    description: str
    topics: List[str]


@app.get("/api/committees", response_model=List[Committee])
def get_committees():
    return [
        Committee(
            code="UNGA",
            name="United Nations General Assembly",
            description="Global deliberative body addressing pressing international issues.",
            topics=[
                "Cybersecurity and State Sovereignty",
                "Climate-Induced Migration and International Responsibility"
            ],
        ),
        Committee(
            code="UNHRC",
            name="United Nations Human Rights Council",
            description="Protecting and promoting human rights around the world.",
            topics=[
                "Digital Surveillance and Privacy Rights",
                "Human Rights of Refugees and Asylum Seekers"
            ],
        ),
        Committee(
            code="UNSC",
            name="United Nations Security Council",
            description="Maintenance of international peace and security.",
            topics=[
                "Security Implications of Autonomous Weapons",
                "Stability in the South China Sea"
            ],
        ),
        Committee(
            code="IP",
            name="International Press",
            description="Journalistic coverage, interviews and real-time updates during the conference.",
            topics=[
                "Press ethics in conflict reporting",
                "Combating misinformation during crises"
            ],
        ),
    ]


# Registration endpoint
@app.post("/api/registrations")
def create_registration(payload: Delegate):
    try:
        doc_id = create_document("delegate", payload)
        return {"status": "success", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
