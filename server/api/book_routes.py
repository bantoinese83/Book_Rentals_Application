# book_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from security.auth import get_current_user
from models.user import User
from schemas.book import BookCreate, BookUpdate
from services import book_service
from typing import List

router = APIRouter()


@router.post("/books/", tags=["Books"])
async def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return book_service.create_book(db, book)


@router.put("/books/{book_id}", tags=["Books"])
async def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return book_service.update_book(db, book_id, book)


@router.delete("/books/{book_id}", tags=["Books"])
async def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return book_service.delete_book(db, book_id)


@router.get("/books/{book_id}", tags=["Books"])
async def get_book(book_id: int, db: Session = Depends(get_db)):
    return book_service.get_book(db, book_id)


@router.get("/books/", tags=["Books"])
async def list_books(db: Session = Depends(get_db)):
    return book_service.list_books(db)


@router.post("/rentals/{book_id}", tags=["Rentals"])
async def rent_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rental = book_service.rent_book(db, book_id, current_user.id)
    if rental is None:
        raise HTTPException(status_code=404, detail="Book not available")
    return rental


@router.put("/rentals/{rental_id}", tags=["Rentals"])
async def return_book(rental_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rental = book_service.return_book(db, rental_id, current_user.id)
    if rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental


@router.get("/rentals/", tags=["Rentals"])
async def list_rentals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return book_service.list_rentals(db, current_user.id)


@router.post("/books/bulk", tags=["Books"])
async def create_books(books: List[BookCreate], db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return book_service.save_book_list(db, books)
