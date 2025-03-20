from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database, auth
from typing import List

router = APIRouter(prefix="/answers", tags=["answers"])

@router.post("/", response_model=schemas.Answer)
def create_answer(answer: schemas.AnswerCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    question = crud.get_question(db, answer.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return crud.create_answer(db=db, answer=answer, owner_id=current_user.id)

@router.get("/{question_id}", response_model=List[schemas.Answer])
def read_answers_by_question(question_id: int, db: Session = Depends(database.get_db)):
    question = crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return crud.get_answers_by_question(db, question_id=question_id)

@router.put("/{answer_id}", response_model=schemas.Answer)
def update_answer(answer_id: int, answer: schemas.AnswerCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    db_answer = crud.get_answer(db, answer_id=answer_id)
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    if db_answer.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.update_answer(db, answer_id=answer_id, answer=answer)

@router.delete("/{answer_id}", status_code=204)
def delete_answer(answer_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    db_answer = crud.get_answer(db, answer_id=answer_id)
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    if db_answer.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    crud.delete_answer(db, answer_id=answer_id)