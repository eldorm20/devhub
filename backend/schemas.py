# filepath: /workspaces/devhub/backend/schemas.py
from pydantic import BaseModel
from typing import Optional

# User schemas
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

# Question schemas
class QuestionBase(BaseModel):
    title: str
    content: str

class QuestionCreate(QuestionBase):
    tags: Optional[str] = None

# Discussion schemas
class DiscussionBase(BaseModel):
    title: str
    content: str

class DiscussionCreate(DiscussionBase):
    pass

# Answer schemas
class AnswerBase(BaseModel):
    content: str

class AnswerCreate(AnswerBase):
    pass

# Comment schemas
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    question_id: Optional[int] = None
    discussion_id: Optional[int] = None
    answer_id: Optional[int] = None