from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database, auth, meilisearch_client
from typing import List

router = APIRouter(prefix="/discussions", tags=["discussions"])

@router.post("/", response_model=schemas.Discussion)
def create_discussion(discussion: schemas.DiscussionCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    db_discussion = crud.create_discussion(db=db, discussion=discussion, owner_id=current_user.id)
    meilisearch_client.index_discussion(db_discussion.__dict__)
    return db_discussion

@router.get("/", response_model=List[schemas.Discussion])
def read_discussions(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_discussions(db, skip=skip, limit=limit)

@router.get("/{discussion_id}", response_model=schemas.Discussion)
def read_discussion(discussion_id: int, db: Session = Depends(database.get_db)):
    db_discussion = crud.get_discussion(db, discussion_id=discussion_id)
    if db_discussion is None:
        raise HTTPException(status_code=404, detail="Discussion not found")
    return db_discussion

@router.get("/search/{query}")
def search_discussion(query: str):
    return meilisearch_client.search_discussions(query)

@router.put("/{discussion_id}", response_model=schemas.Discussion)
def update_discussion(discussion_id: int, discussion: schemas.DiscussionCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    db_discussion = crud.get_discussion(db, discussion_id=discussion_id)
    if db_discussion is None:
        raise HTTPException(status_code=404, detail="Discussion not found")
    if db_discussion.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db_discussion = crud.update_discussion(db, discussion_id=discussion_id, discussion=discussion)
    meilisearch_client.index_discussion(db_discussion.__dict__)
    return db_discussion

@router.delete("/{discussion_id}", status_code=204)
def delete_discussion(discussion_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    db_discussion = crud.get_discussion(db, discussion_id=discussion_id)
    if db_discussion is None:
        raise HTTPException(status_code=404, detail="Discussion not found")
    if db_discussion.owner_id != current_user.id:
        raise HTTPException