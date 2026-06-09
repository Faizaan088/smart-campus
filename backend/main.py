from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import datetime
from database import engine ,Base ,Sessionlocal
import models
from models import User , Complaint
Base.metadata.create_all(bind=engine)
class ComplaintCreate(BaseModel):
    title: str
    description: str
    suggested_solution: Optional[str] = None
class StatusUpdate(BaseModel):
    status: str
app=FastAPI()
@app.get("/")
def home():
    return {"message":"Welcome to the Smart Campuse Management System"}
complaints =   [
            {
                "id":1,
                "title":"wifi not working",
                "description":"The wifi in the library is not working.",
                "status":"open",
                "suggested_solution":"Check the router and reset it if necessary.",
                "category":"IT",
                "created_at":"2024-06-01T10:00:00Z"
        },
        {
                "id":2,
                "title":"washing machine not working",
                "description":"The washing machine in the coridor is not working.",
                "status":"open",
                "suggested_solution":"Check the machine and reset it if necessary.",
                "category":"mechanical",
                "created_at":"2024-06-01T10:00:00Z"
        } ]
@app.get("/complaints")
def get_complaints():
    session=Sessionlocal()
    que=session.query(Complaint)
    com=que.all()
    res = []
    for c in com:
        res.append({
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "status": c.status,
            "category": c.category,
            "priority": c.priority,
            "user_id": c.user_id,
            "created_at": c.created_at
        })

    session.close()
    return {"complaints": res}
@app.get("/complaints/{complaint_id}")
def get_complaint(complaint_id:int):
    session=Sessionlocal()
    que=session.query(Complaint)
    com=que.all()
    for complaint in complaints:
        if complaint["id"] == complaint_id:
            return {
                "complaint": complaint
            }
    return {"error": "Complaint not found"}
@app.post("/complaints")
def create_complaint(complaint: ComplaintCreate):
    complaint = complaint.model_dump()
    complaint["id"] = len(complaints) + 1
    status = "open"
    complaint["status"] = status
    category = None
    complaint["category"] = category
    priority = None
    complaint["priority"] = priority
    created_at = datetime.datetime.now().isoformat()
    complaint["created_at"] = created_at
    complaints.append(complaint)
    return {
        "message": "Complaint created successfully",
        "complaint": complaint
    }
@app.put("/complaints/{complaint_id}")
def update_complaint(complaint_id: int, complaint: StatusUpdate):
    for i in complaints:
            if i["id"]==complaint_id:
                i["status"]=complaint.status
                return {
                    "message":"Complaint updated successfully",
                    "complaint":i
            }
    return {"error":"Complaint not found"}
@app.delete("/complaints/{complaint_id}")
def delete_complaint(complaint_id: int):
    for i in complaints:
        if i["id"]==complaint_id:
            complaints.remove(i)
            return {
                "message":"Complaint deleted successfully"
            }
    return {"error":"Complaint not found"}