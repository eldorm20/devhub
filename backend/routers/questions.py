from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database, auth, meilisearch_client
from typing import List

router = APIRouter(prefix="/questions", tags=["questions"])

@router.post("/", response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    db_question = crud.create_question(db=db, question=question, owner_id=current_user.id)
    meilisearch_client.index_question(db_question.__dict__)
    return db_question

@router.get("/", response_model=List[schemas.Question])
def read_questions(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_questions(db, skip=skip, limit=limit)

@router.get("/{question_id}", response_model=schemas.Question)
def read_question(question_id: int, db: Session = Depends(database.get_db)):
    db_question = crud.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

@router.get("/search/{query}")
def search_question(query: str):
    return meilisearch_client.search_questions(query)