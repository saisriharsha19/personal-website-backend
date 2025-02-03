from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# SQLAlchemy Models
class DBPortfolioItem(Base):
    __tablename__ = "portfolio_items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(Text)
    image_url = Column(String(400))
    project_url = Column(String(200))

class DBBlogPost(Base):
    __tablename__ = "blog_posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(Text)
    author = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)

class DBContactMessage(Base):
    __tablename__ = "contact_messages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    subject = Column(String(200), nullable=True)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    email_sent = Column(Boolean, default=False)

# Pydantic Schemas
class PortfolioItemBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: str
    image_url: str = Field(..., max_length=400)
    project_url: str = Field(..., max_length=200)

class PortfolioItemCreate(PortfolioItemBase):
    pass

class PortfolioItem(PortfolioItemBase):
    id: int
    class Config:
        orm_mode = True

class BlogPostBase(BaseModel):
    title: str = Field(..., max_length=200)
    content: str
    author: str = Field(..., max_length=100)

class BlogPostCreate(BlogPostBase):
    class Config:
        orm_mode = True

class BlogPost(BlogPostBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class ContactMessageBase(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str

class ContactMessageCreate(ContactMessageBase):
    pass

class ContactMessage(ContactMessageBase):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str

    class Config:
        orm_mode = True


class ContactMessageResponse(BaseModel):
    id: int
    name: str
    email: str
    message: str
    created_at: datetime
    email_sent: bool
    subject: Optional[str] = None
    class Config:
        orm_mode = True