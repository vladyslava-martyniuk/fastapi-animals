from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Animal

# Створення таблиць (але Alembic вже зробив це)
Base.metadata.create_all(bind=engine)

# ----------------------
# Pydantic-моделі
# ----------------------
class AnimalResponse(BaseModel):
    id: int
    name: str
    age: int
    adopted: bool
    health_status: str

    class Config:
        orm_mode = True

class AnimalCreate(BaseModel):
    name: str = Field(..., example="Charlie")
    age: int = Field(..., ge=0, example=2)
    adopted: bool = Field(default=False)
    health_status: str = Field(default="healthy", example="healthy")

# ----------------------
# FastAPI
# ----------------------
app = FastAPI(title="Animals API")

# Додаємо першого тварину при старті сервера
@app.on_event("startup")
def add_first_animal():
    db: Session = SessionLocal()
    if not db.query(Animal).first():
        new_animal = Animal(
            name="Buddy",
            age=3,
            adopted=False,
            health_status="healthy"
        )
        db.add(new_animal)
        db.commit()
    db.close()

# ----------------------
# GET: всі тварини
# ----------------------
@app.get("/animals", response_model=list[AnimalResponse])
def get_animals():
    db: Session = SessionLocal()
    animals = db.query(Animal).all()
    db.close()
    return animals

# ----------------------
# POST: додати нову тварину
# ----------------------
@app.post("/animals", response_model=AnimalResponse)
def create_animal(animal: AnimalCreate):
    if animal.age < 0:
        raise HTTPException(status_code=400, detail="Age cannot be negative")
    db: Session = SessionLocal()
    new_animal = Animal(
        name=animal.name,
        age=animal.age,
        adopted=animal.adopted,
        health_status=animal.health_status
    )
    db.add(new_animal)
    db.commit()
    db.refresh(new_animal)
    db.close()
    return new_animal
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)