from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database, auth
from typing import List

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return crud.create_comment(db=db, comment=comment, owner_id=current_user.id)

@router.get("/question/{question_id}", response_model=List[schemas.Comment])
def read_comments_by_question(question_id: int, db: Session = Depends(database.get_db)):
    return crud.get_comments_by_question(db, question_id=question_id)

@router.get("/discussion/{discussion_id}", response_model=List[schemas.Comment])
def read_comments_by_discussion(discussion_id: int, db: Session = Depends(database.get_db)):
    return crud.get_comments_by_discussion(db, discussion_id=discussion_id)

@router.get("/answer/{answer_id}", response_model=List[schemas.Comment])
def read_comments_by_answer(answer_id: int, db: Session = Depends(database.get_db)):
    return crud.get_comments_by_answer(db, answer_id=answer_id)

@router.put("/{comment_id}", response_model=schemas.Comment)
def update_comment(comment_id: int, comment: schemas.CommentCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.update_comment(db, comment_id=comment_id, comment=comment)

@router.delete("/{comment_id}", status_code=204)
def delete_comment(comment_id