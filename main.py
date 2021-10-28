import uvicorn
from fastapi import FastAPI, status, HTTPException
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
    # create a db session for committing 
    session = Session(bind=engine, expire_on_commit=False)
    
    # get item with id given
    todo = session.query(ToDo).get(id)
       
    # close the session
    session.close()    
  
    # return task info
    if todo:
        return f"task is with id {todo.id} is {todo.task}"
    else:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

@app.put("/todo/{id}")
def update_todo(id: int, task:str):
    print(task)
     # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo item with the given id
    todo = session.query(ToDo).get(id)    
    
    if todo:
        todo.task = task
        session.commit()     
    
    # close the session
    session.close()
    
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")
    
    return todo
    
  
    
    return f"update todo item with id {id}"

@app.delete("/todo/{id}")
def delete_todo(id: int):
    return f"delete todo item with id {id}"

@app.get("/todo")
def read_todo_list():
     # create a new database session
    session = Session(bind=engine, expire_on_commit=False)
    
    # get todo all items
    todo_list = session.query(ToDo).all()
        
    # dont forget to close the session
    # we better change it "with"
    session.close() 
    
    return todo_list

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)