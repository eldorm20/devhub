from sqlalchemy.orm import Session
from backend.models import User, Question, Discussion, Answer, Comment
from backend.schemas import DiscussionCreate, UserCreate, QuestionCreate
from passlib.context import CryptContext
from sqlalchemy import func

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User CRUD Operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Question CRUD Operations
def create_question(db: Session, question: schemas.QuestionCreate, owner_id: int):
    db_question = models.Question(**question.dict(), owner_id=owner_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Question).offset(skip).limit(limit).all()

def get_question(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id).first()

def update_question(db: Session, question_id: int, question: schemas.QuestionCreate):
    db_question = get_question(db, question_id)
    if db_question:
        for key, value in question.dict().items():
            setattr(db_question, key, value)
        db_question.updated_at = func.now()
        db.commit()
        db.refresh(db_question)
    return db_question

def delete_question(db: Session, question_id: int):
    db_question = get_question(db, question_id)
    if db_question:
        db.delete(db_question)
        db.commit()

# Discussion CRUD Operations
def create_discussion(db: Session, discussion: schemas.DiscussionCreate, owner_id: int):
    db_discussion = models.Discussion(**discussion.dict(), owner_id=owner_id)
    db.add(db_discussion)
    db.commit()
    db.refresh(db_discussion)
    return db_discussion

def get_discussions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Discussion).offset(skip).limit(limit).all()

def get_discussion(db: Session, discussion_id: int):
    return db.query(models.Discussion).filter(models.Discussion.id == discussion_id).first()

def update_discussion(db: Session, discussion_id: int, discussion: schemas.DiscussionCreate):
    db_discussion = get_discussion(db, discussion_id)
    if db_discussion:
        for key, value in discussion.dict().items():
            setattr(db_discussion, key, value)
        db_discussion.updated_at = func.now()
        db.commit()
        db.refresh(db_discussion)
    return db_discussion

def delete_discussion(db: Session, discussion_id: int):
    db_discussion = get_discussion(db, discussion_id)
    if db_discussion:
        db.delete(db_discussion)
        db.commit()

# Answer CRUD Operations
def create_answer(db: Session, answer: schemas.AnswerCreate, owner_id: int):
    db_answer = models.Answer(**answer.dict(), owner_id=owner_id)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def get_answers_by_question(db: Session, question_id: int):
    return db.query(models.Answer).filter(models.Answer.question_id == question_id).all()

def get_answer(db: Session, answer_id: int):
    return db.query(models.Answer).filter(models.Answer.id == answer_id).first()

def update_answer(db: Session, answer_id: int, answer: schemas.AnswerCreate):
    db_answer = get_answer(db, answer_id)
    if db_answer:
        for key, value in answer.dict().items():
            setattr(db_answer, key, value)
        db_answer.updated_at = func.now()
        db.commit()
        db.refresh(db_answer)
    return db_answer

def delete_answer(db: Session, answer_id: int):
    db_answer = get_answer(db, answer_id)
    if db_answer:
        db.delete(db_answer)
        db.commit()

# Comment CRUD Operations
def create_comment(db: Session, comment: schemas.CommentCreate, owner_id: int):
    db_comment = models.Comment(**comment.dict(), owner_id=owner_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_by_question(db: Session, question_id: int):
    return db.query(models.Comment).filter(models.Comment.question_id == question_id).all()

def get_comments_by_discussion(db: Session, discussion_id: int):
    return db.query(models.Comment).filter(models.Comment.discussion_id == discussion_id).all()

def get_comments_by_answer(db: Session, answer_id: int):
    return db.query(models.Comment).filter(models.Comment.answer_id == answer_id).all()

def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def update_comment(db: Session, comment_id: int, comment: schemas.CommentCreate):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        for key, value in comment.dict().items():
            setattr(db_comment, key, value)
        db_comment.updated_at = func.now()
        db.commit()
        db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        db.delete(db_comment)
        db.commit()