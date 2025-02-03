from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_portfolio_items, get_db
from app.models import PortfolioItem, DBPortfolioItem, PortfolioItemCreate
from typing import List

router = APIRouter(tags=["Portfolio"])



@router.get("/", response_model=List[PortfolioItem])
async def get_portfolio_items_route():
    try:
        items = get_portfolio_items() 
        return items
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving portfolio items: {str(e)}"
        )

@router.post("/", response_model=PortfolioItem, status_code=status.HTTP_201_CREATED)
async def create_portfolio_item(item: PortfolioItemCreate, db: Session = Depends(get_db)):
    try:
        new_item = DBPortfolioItem(
            title=item.title,
            description=item.description,
            image_url=item.image_url,
            project_url=item.project_url
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating portfolio item: {str(e)}"
        )

@router.delete("/portfolio-items/{item_id}")
def delete_portfolio_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(DBPortfolioItem).filter(DBPortfolioItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio item not found"
        )
    db.delete(item)
    db.commit()
    return {"message": "Portfolio item deleted successfully"}