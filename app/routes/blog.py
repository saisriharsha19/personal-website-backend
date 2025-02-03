from fastapi import APIRouter, HTTPException, status, Depends
from app.database import get_blog_posts, get_db
from app.models import BlogPost, BlogPostCreate, DBBlogPost
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(tags=["Blog"])

@router.get("/", response_model=List[BlogPost])
async def get_blog_posts_route():
    try:
        posts = get_blog_posts()  # Use the database function
        return posts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving blog posts: {str(e)}"
        )

@router.get("/{blog_id}")
async def get_blog_post_by_id(blog_id: int, db: Session = Depends(get_db)):
    post = db.query(DBBlogPost).filter(DBBlogPost.id == blog_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )
    return post

@router.post("/blog-posts/")
def create_blog_post(item:BlogPostCreate, db: Session = Depends(get_db)):
    new_post = DBBlogPost(title=item.title, content=item.content, author=item.author)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/blogs/{blog_id}")
def delete_blog_post(blog_id: int, db: Session = Depends(get_db)):
    post = db.query(DBBlogPost).filter(DBBlogPost.id == blog_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )
    db.delete(post)
    db.commit()
    return {"message": "Blog post deleted successfully"}


