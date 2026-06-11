from fastapi import FastAPI , HTTPException
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
    user_id : int
    suggested_solution: Optional[str] = None

class ComplaintUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    user_id : Optional[int] = None
    suggested_solution: Optional[str] = None
    status: Optional[str] = None
    category : Optional[str] = None
    priority : Optional[str] = None

class UserCreate(BaseModel):
    name : str
    email : str
    password : str   
    role : str

class UserUpdate(BaseModel):
    name : Optional[str] = None
    email : Optional[str] = None
    password : Optional[str] = None
    role : Optional[str] = None

app=FastAPI()

@app.get("/")
def home():
    return {"message":"Welcome to the Smart Campuse Management System"}

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
            "created_at": c.created_at,
            "suggested_solution" : c.suggested_solution
        })

    session.close()
    return {"complaints": res}

@app.get("/complaints/{complaint_id}")
def get_complaint(complaint_id:int):
    session=Sessionlocal()
    que=session.query(Complaint)
    com=que.filter(Complaint.id==complaint_id).first()
    session.close()
    if com:
        return {
            "complaint": {
                "id": com.id,
                "title": com.title,
                "description": com.description,
                "status": com.status,
                "category": com.category,
                "priority": com.priority,
                "user_id": com.user_id,
                "created_at": com.created_at,
                "suggested_solution" : com.suggested_solution
            }
        }
    raise HTTPException(
    status_code=404,
    detail="Complaint not found"
)

@app.get("/users")
def get_users():
    session = Sessionlocal()
    user = session.query(User)
    users = user.all()
    res = []
    for c in users:
        res.append({
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "role": c.role,
        })
    session.close()
    return {"users": res}

@app.get("/users/{user_id}")
def get_user(user_id:int):
    session=Sessionlocal()
    que=session.query(User)
    c=que.filter(User.id==user_id).first()
    session.close()
    if c:
        return {
            "user": {
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "role": c.role,
            }
        }
    raise HTTPException(
    status_code=404,
    detail="User not found"
)
  
@app.post("/complaints")
def create_complaint(complaint: ComplaintCreate):
    session = Sessionlocal()
    new_complaint = Complaint(
        title = complaint.title,
        description = complaint.description,
        user_id = complaint.user_id,
        status = "open",
        category = None,
        priority = None,
        created_at = datetime.datetime.now().isoformat(),
        suggested_solution = complaint.suggested_solution
    )
    session.add(new_complaint)
    session.commit()
    id=new_complaint.id
    session.close()
    return {
        "message": "Complaint created successfully",
        "id":id
    }

@app.post("/users")
def create_user(user: UserCreate):
    session = Sessionlocal()
    new_user = User(
        name = user.name,
        email = user.email,
        password = user.password,
        role = user.role
    )
    session.add(new_user)
    session.commit()
    id=new_user.id
    session.close()
    return{
        "message": "User added successfully",
        "id":id
    }

@app.put("/complaints/{complaint_id}")
def update_complaint(complaint_id: int, complaint: ComplaintUpdate):
    session = Sessionlocal()
    que = session.query(Complaint)
    com = que.filter(Complaint.id == complaint_id).first()
    if com:
        if complaint.status is not None:
            com.status = complaint.status
        if complaint.title is not None:
            com.title = complaint.title
        if complaint.description is not None:
            com.description = complaint.description
        if complaint.category is not None:
            com.category = complaint.category
        if complaint.priority is not None:
            com.priority = complaint.priority
        if complaint.user_id is not None:
            com.user_id = complaint.user_id
        if complaint.suggested_solution is not None:
            com.suggested_solution = complaint.suggested_solution
        session.commit()
        session.close()
        return {
                    "message":"Complaint updated successfully",
            }
    session.close()
    raise HTTPException(
    status_code=404,
    detail="Complaint not found"
)

@app.put("/users/{user_id}")
def update_user(user_id : int , user: UserUpdate):
    session = Sessionlocal()
    que = session.query(User)
    use = que.filter(User.id == user_id).first()
    if use:
        if user.name:
            use.name = user.name
        if user.email:
            use.email = user.email
        if user.password:
            use.password = user.password
        if user.role:
            use.role = user.role       
        session.commit()
        session.close()
        return {
                    "message":"User updated successfully",
            }
    session.close()
    raise HTTPException(
    status_code=404,
    detail="User not found"
)

@app.delete("/complaints/{complaint_id}")
def delete_complaint(complaint_id: int):
    session = Sessionlocal()
    que = session.query(Complaint)
    com = que.filter(Complaint.id == complaint_id).first()
    if com:
        session.delete(com)
        session.commit()
        session.close()
        return {
                "message":"Complaint deleted successfully"
            }
    session.close()
    raise HTTPException(
    status_code=404,
    detail="Complaint not found"
)

@app.delete("/users/{user_id}")
def delete_user(user_id:int):
    session = Sessionlocal()
    que = session.query(User)
    use = que.filter(User.id == user_id).first()
    if use:
        session.delete(use)
        session.commit()
        session.close()
        return{
            "message":"User deleted successfully"
        }
    session.close()
    raise HTTPException(
    status_code=404,
    detail="User not found"
)

@app.get("/users/{user_id}/complaints")
def get_users_complaint(user_id:int):
    session = Sessionlocal()
    que = session.query(User)
    use = que.filter(User.id == user_id).first()
    res = []
    if use is not None:
        com = use.complaints
        for c in com:
            res.append({
                "id": c.id,
                "title": c.title,
                "description": c.description,
                "status": c.status,
                "category": c.category,
                "priority": c.priority,
                "user_id": c.user_id,
                "created_at": c.created_at,
                "suggested_solution" : c.suggested_solution
            })  
        session.close()
        return {"complaints":res}
    session.close()
    raise HTTPException(
    status_code=404,
    detail="User not found"
)   

@app.get("/complaints/{complaint_id}/user")
def get_complaint_user(complaint_id:int):
    session = Sessionlocal()
    que=session.query(Complaint)
    com = que.filter(Complaint.id == complaint_id).first()
    if com is not None:
        use = com.user
        session.close()
        return {
                "user": {
                    "id": use.id,
                    "name": use.name,
                    "email": use.email,
                    "role": use.role,
            }
        }   
    session.close()
    raise HTTPException(
    status_code=404,
    detail="Complaint not found"
)