import uvicorn
from fastapi import FastAPI, status
from database import Base, engine, ToDo
from pydantic import BaseModel
from sqlalchemy.orm import Session, session

# Create ToDoRequest Base Model
class ToDoRequest(BaseModel):
    task: str

# Create the database
Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
def root():
    return "todooo"

@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: ToDoRequest):
    print(todo.task)
    # create a db session for committing 
    session = Session(bind=engine, expire_on_commit=False)
    
    # create an ToDo model instance
    tododb = ToDo(task=todo.task)
    
    # lets add instance to current session    
    session.add(tododb)
    
    # commit changes to db
    session.commit()
    
    # get id of newly created record
    id = tododb.id
    
    # close the session
    session.close()    
        
    return f" create todo item with id {id}"

@app.get("/todo/{id}")
def read_todo(id: int):
    return "read todo item with id {id}"

@app.put("/todo/{id}")
def update_todo(id: int):
    return "update todo item with id {id}"

@app.delete("/todo/{id}")
def delete_todo(id: int):
    return "delete todo item with id {id}"

@app.get("/todo")
def read_todo_list():
    return "read todo list"

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)