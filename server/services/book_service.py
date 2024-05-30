from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.book import Book
from models.rental import Rental
from models.renter import Renter
from schemas.book import BookCreate, BookUpdate


def create_book(db: Session, book: BookCreate):
    try:
        db_book = Book(**book.dict(), quantity=1)  # Set default quantity to 1
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def update_book(db: Session, book_id: int, book: BookUpdate):
    try:
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if db_book is None:
            raise ValueError(f"Book with id {book_id} not found")
        for var, value in vars(book).items():
            setattr(db_book, var, value) if value else None
        if book.quantity:  # Update quantity if provided
            db_book.quantity = book.quantity
        db.commit()
        return db_book
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def delete_book(db: Session, book_id: int):
    try:
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if db_book is None:
            raise ValueError(f"Book with id {book_id} not found")
        db.delete(db_book)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def list_books(db: Session):
    return db.query(Book).all()


def rent_book(db: Session, book_id: int, renter_id: int) -> Optional[Rental]:
    try:
        # Retrieve book and renter information
        db_book = db.query(Book).filter(Book.id == book_id).first()
        db_renter = db.query(Renter).filter(Renter.id == renter_id).first()

        # Check if book and renter exist
        if not db_book:
            raise ValueError(f"Book with id {book_id} not found")
        if not db_renter:
            raise ValueError(f"Renter with id {renter_id} not found")

        # Check if the book is available for rent
        if db_book.quantity <= 0:
            raise ValueError(f"Book with id {book_id} is not available for rent")

        # Check if the renter has already rented the same book and not returned it
        existing_rental = db.query(Rental).filter(
            and_(
                Rental.book_id == book_id,
                Rental.renter_id == renter_id,
                Rental.return_date.is_(None)
            )
        ).first()
        if existing_rental:
            raise ValueError("You have already rented this book and not returned it")

        # Create a new rental record
        rental = Rental(renter_id=renter_id, book_id=book_id)
        db.add(rental)

        # Decrease the quantity of the book
        db_book.quantity -= 1

        db.commit()
        return rental
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def return_book(db: Session, rental_id: int, renter_id: int):
    try:
        rental = db.query(Rental).filter(
            and_(
                Rental.id == rental_id,
                Rental.renter_id == renter_id
            )
        ).first()
        if rental is None or rental.return_date is not None:
            raise ValueError(f"Rental with id {rental_id} not found or already returned")

        # Increase the quantity of the book
        rental.book.quantity += 1

        # Update the return date of the rental
        rental.return_date = datetime.utcnow()

        db.commit()
        return rental
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def list_rentals(db: Session, renter_id: int):
    return db.query(Rental).filter(Rental.renter_id == renter_id).all()


def save_book_list(db: Session, book_list: List[BookCreate]):
    try:
        db_books = [Book(**book.dict()) for book in book_list]
        db.add_all(db_books)
        db.commit()
        for book in db_books:
            db.refresh(book)
        return db_books
    except SQLAlchemyError as e:
        db.rollback()
        raise e
