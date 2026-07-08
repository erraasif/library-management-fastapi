from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="Library Management System")

# --- Pydantic Schemas ---
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, examples=["The Hobbit"])
    author: str = Field(..., min_length=1, examples=["J.R.R. Tolkien"])
    published_year: int = Field(..., gt=0, examples=[1937])
    genre: str = Field(..., min_length=1, examples=["Fantasy"])
    is_available: bool = Field(default=True)

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1)
    published_year: Optional[int] = Field(None, gt=0)
    genre: Optional[str] = Field(None, min_length=1)
    is_available: Optional[bool] = None

class BookResponse(BookBase):
    id: int

# --- In-Memory Database Simulation ---
db_books = {}
id_counter = 1

# --- CRUD Endpoints ---

# CREATE: Add a new book
@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    global id_counter
    new_book = BookResponse(id=id_counter, **book.model_dump())
    db_books[id_counter] = new_book
    id_counter += 1
    return new_book

# READ ALL: Get all books
@app.get("/books", response_model=List[BookResponse])
def get_all_books():
    return list(db_books.values())

# READ ONE: Get a single book by ID
@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    if book_id not in db_books:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")
    return db_books[book_id]

# UPDATE: Modify an existing book (Partial updates supported)
@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookUpdate):
    if book_id not in db_books:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")
    
    current_book_dict = db_books[book_id].model_dump()
    update_data = book_update.model_dump(exclude_unset=True)
    
    # Overwrite old data with new data
    current_book_dict.update(update_data)
    
    updated_book = BookResponse(**current_book_dict)
    db_books[book_id] = updated_book
    return updated_book

# DELETE: Remove a book by ID
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    if book_id not in db_books:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")
    del db_books[book_id]
    return None