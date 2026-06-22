from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from typing import Optional
import datetime
from database import engine ,Base ,Sessionlocal
import models
from models import User , Complaint , Resource , Booking 
from enum import Enum 
Base.metadata.create_all(bind=engine)

class ComplaintStatus(str , Enum):
    PENDING      = "pending"
    OPEN         = "open"
    IN_PROGRESS  = "in_progress"
    RESOLVED     = "resolved"
    REOPENED     = "reopened"
    REJECTED     = "rejected"

class ComplaintCategory(str , Enum):
    IT_CSE = "IT/CSE"
    ELECTRICAL = "Electrical"
    MECHANICAL = "Mechanical"
    CIVIL = "Civil"
    HOSTEL = "Hostel"
    LIBRARY = "Library"
    ADMINISTRATION = "Administration"
    OTHER = "Other"

class ComplaintPriority(str , Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class UserRole(str , Enum):
    STUDENT = "student"
    ADMIN = "admin"

class ResourceStatus(str , Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    RETURNED = "returned"

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
    status: Optional[ComplaintStatus] = None
    category : Optional[ComplaintCategory] = None
    priority : Optional[ComplaintPriority] = None

class UserCreate(BaseModel):
    name : str
    email : str
    password : str   
    role : UserRole

class UserUpdate(BaseModel):
    name : Optional[str] = None
    email : Optional[str] = None
    password : Optional[str] = None
    role : Optional[UserRole] = None

class ResourceCreate(BaseModel):
    name : str
    type : str
    available_quantity : int

class ResourceUpdate(BaseModel):
    name : Optional[str] = None
    type : Optional[str] = None
    available_quantity : Optional[int] = None

class BookingCreate(BaseModel):
    user_id : int
    resource_id : int
    purpose : str
    remark : str
    booking_date : str
    time_slot : str

class BookingUpdate(BaseModel):
    user_id : Optional[int] = None
    resource_id : Optional[int] = None
    status : Optional[ResourceStatus] = None
    purpose : Optional[str] = None
    remark : Optional[str] = None
    booking_date : Optional[str] = None
    time_slot : Optional[str] = None

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
        status = "pending",
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

@app.get("/resources")
def get_resources():
    session = Sessionlocal()
    que = session.query(Resource)
    res = que.all()
    ans = []
    for r in res:
        ans.append({
            "id" : r.id,
            "name" : r.name,
            "type" : r.type,
            "available_quantity" : r.available_quantity
        })
    session.close()
    return {"Resources" : ans}

@app.get("/resources/{resource_id}")
def get_resource(resource_id : int):
    session = Sessionlocal()
    que = session.query(Resource)
    res = que.filter(Resource.id == resource_id).first()
    session.close()
    if res:
        return{
            "resource":{
            "id" : res.id,
            "name" : res.name,
            "type" : res.type,
            "available_quantity" : res.available_quantity
            }
        }
    raise HTTPException(
    status_code=404,
    detail="Resource not found"
)

@app.post("/resources")
def create_resource(resource : ResourceCreate):
    session = Sessionlocal()
    new_resource = Resource(
        name =  resource.name ,
        type = resource.type,
        available_quantity = resource.available_quantity
    )
    session.add(new_resource)
    session.commit()
    id = new_resource.id
    session.close()
    return {
        "message": "Resource created successfully",
        "id":id
    } 

@app.put("/resources/{resource_id}")
def update_resources(resource_id : int , resource : ResourceUpdate ):
    session = Sessionlocal()
    que = session.query(Resource)
    res = que.filter(Resource.id == resource_id ).first()
    if res:
        if resource.name is not None:
            res.name = resource.name
        if resource.type is not None:
            res.type = resource.type
        if resource.available_quantity is not None:
            res.available_quantity = resource.available_quantity
        session.commit()
        session.close()
        return {
                    "message":"Resource updated successfully",
            }
    session.close()
    raise HTTPException(
    status_code=404,
    detail="Resource not found"
)

@app.delete("/resources/{resource_id}")
def delete_resource(resource_id : int):
    session = Sessionlocal()
    que = session.query(Resource)
    res = que.filter(Resource.id == resource_id).first()
    if res:
        session.delete(res)
        session.commit()
        session.close()
        return{
            "message":"Resource deleted succesfully"
        }
    session.close()
    raise HTTPException(
    status_code=404,
    detail="Resource not found"
)   

@app.get("/bookings")
def get_bookings():
    session = Sessionlocal()
    que = session.query(Booking)
    boo = que.all()
    res = []
    for b in boo:
        res.append({
            "id" : b.id,
            "user_id" : b.user_id,
            "resource_id" : b.resource_id,
            "status" : b.status , 
            "purpose" : b.purpose ,
            "remark" : b.remark ,
            "booking_date" : b.booking_date ,
            "time_slot" : b.time_slot
        })
    session.close()
    return {"bookings": res}

@app.get("/bookings/{booking_id}")
def get_booking(booking_id : int):
    session = Sessionlocal()
    que = session.query(Booking)
    boo = que.filter(Booking.id == booking_id).first()
    session.close()
    if boo:
        return {
            "Booking":{
                "id" : boo.id ,
                "user_id" : boo.user_id,
                "resource_id" : boo.resource_id,
                "status" : boo.status , 
                "purpose" : boo.purpose ,
                "remark" : boo.remark ,
                "booking_date" : boo.booking_date ,
                "time_slot" : boo.time_slot               
            }
        }
    raise HTTPException(
    status_code=404,
    detail="Booking not found"
)

@app.post("/bookings")
def create_booking(booking : BookingCreate):
    session = Sessionlocal()
    que = session.query(User)
    qu = session.query(Resource)
    use = que.filter(User.id == booking.user_id).first()
    re = qu.filter(Resource.id == booking.resource_id).first()
    if use is None:
        session.close()
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if re is None:
        session.close()
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )
    if(re.available_quantity<=0):
        session.close()
        raise HTTPException(
            status_code=400,
            detail="Resource unavailable"
        )
    new_booking = Booking(
        user_id = booking.user_id,
        resource_id = booking.resource_id , 
        status = "pending" ,
        purpose = booking.purpose ,
        remark = booking.remark,
        booking_date = booking.booking_date,
        time_slot = booking.time_slot
    )
    session.add(new_booking)
    re.available_quantity-= 1
    session.commit()
    id = new_booking.id
    session.close()
    return{
        "message" : " booking Succesfull",
        "booking id" : id
    }

@app.put("/bookings/{booking_id}")
def update_booking(booking_id :int , booking : BookingUpdate):
    session = Sessionlocal()
    que = session.query(Booking)
    boo = que.filter(Booking.id == booking_id).first()
    if boo:
        if booking.user_id is not None:
            boo.user_id = booking.user_id
        if booking.resource_id is not None:
            boo.resource_id = booking.resource_id 
        if booking.status is not None:
            boo.status = booking.status 
            if booking.status == "reject" or booking.status == "returned" or booking.status == "pending":
                qu =session.query(Resource)
                re = qu.filter(Resource.id == boo.resource_id).first()
                re.available_quantity+=1
        if booking.purpose is not None:
            boo.purpose = booking.purpose         
        if booking.remark is not None:
            boo.remark = booking.remark
        if booking.booking_date is not None:
            boo.booking_date = booking.booking_date
        if booking.time_slot is not None: 
            boo.time_slot = booking.time_slot
        session.commit()
        session.close()
        return {
                    "message":"Booking updated successfully",
            }
    session.close()
    raise HTTPException(
    status_code=404,
    detail="Booking not found"
)        

@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id : int):
    session = Sessionlocal()
    que = session.query(Booking)
    boo = que.filter(Booking.id == booking_id).first()
    if boo:
        qu = session.query(Resource)
        re = qu.filter(Resource.id == boo.resource_id).first()
        re.available_quantity+= 1
        session.delete(boo)
        session.commit()

        session.close()
        return{
            "message":"Booking deleted succesfully"
        }
    session.close()
    raise HTTPException(
    status_code=404,
    detail="Booking not found"
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
                    "role": use.role
            }
        }   
    session.close()
    raise HTTPException(
    status_code=404,
    detail="Complaint not found"
)

@app.get("/resources/{resource_id}/bookings")
def get_resources_booking(resource_id:int):
    session = Sessionlocal()
    que = session.query(Resource)
    re = que.filter(Resource.id == resource_id).first()
    res = []
    if re is not None:
        books = re.bookings
        for b in books:
            res.append({
                "id" : b.id,
                "user_id" : b.user_id,
                "resource_id" : b.resource_id,
                "status" : b.status , 
                "purpose" : b.purpose ,
                "remark" : b.remark ,
                "booking_date" : b.booking_date ,
                "time_slot" : b.time_slot
            })  
        session.close()
        return {"Bookings":res}
    session.close()
    raise HTTPException(
    status_code=404,
    detail="Resource not found"
)   

@app.get("/bookings/{booking_id}/resource")
def get_booking_resource(booking_id:int):
    session = Sessionlocal()
    que=session.query(Booking)
    boo = que.filter(Booking.id == booking_id).first()
    if boo is not None:
        r = boo.resource
        session.close()
        return {
                "resource": {
                    "id" : r.id,
                    "name" : r.name,
                    "type" : r.type,
                    "available_quantity" : r.available_quantity
            }
        }   
    session.close()
    raise HTTPException(
    status_code=404,
    detail="Booking not found"
)

@app.get("/users/{user_id}/bookings")
def get_users_booking(user_id:int):
    session = Sessionlocal()
    que = session.query(User)
    use = que.filter(User.id == user_id).first()
    res = []
    if use is not None:
        boo = use.bookings
        for b in boo:
            res.append({
                "id" : b.id,
                "user_id" : b.user_id,
                "resource_id" : b.resource_id,
                "status" : b.status , 
                "purpose" : b.purpose ,
                "remark" : b.remark ,
                "booking_date" : b.booking_date ,
                "time_slot" : b.time_slot
            })  
        session.close()
        return {"bookings":res}
    session.close()
    raise HTTPException(
    status_code=404,
    detail="User not found"
)   

@app.get("/bookings/{booking_id}/user")
def get_booking_user(booking_id:int):
    session = Sessionlocal()
    que=session.query(Booking)
    boo = que.filter(Booking.id == booking_id).first()
    if boo is not None:
        use = boo.user
        session.close()
        return {
                "user": {
                    "id": use.id,
                    "name": use.name,
                    "email": use.email,
                    "role": use.role
            }
        }   
    session.close()
    raise HTTPException(
    status_code=404,
    detail="Booking not found"
)
