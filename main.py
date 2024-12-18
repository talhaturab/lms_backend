from fastapi import FastAPI, HTTPException
from typing import List
from models import Book, BookCreate, BookUpdate
from pymongo import MongoClient
from bson import ObjectId
from database import uri, db_string, collection_string

app = FastAPI(title="Library Management System", version="1.0")

# MongoDB connection setup
client = MongoClient(uri)
db = client[db_string]
collection = db[collection_string]

@app.on_event("shutdown")
def shutdown_db():
    client.close()
    
# Utility function to convert MongoDB document
def book_helper(book) -> dict:
    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "authors": book["authors"],
        "description": book["description"],
        "category": book["category"],
        "publisher": book["publisher"],
        "publish_date": book["publish_date"],
        "price": book["price"],
        "quantity_available": book["quantity_available"],
        "location": book["location"]
    }

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the Library Management System (LMS)!"}

@app.get("/books/", response_model=List[Book], tags=["Books"])
async def get_all_books():
    try:
        # Use find() instead of aggregate for simplicity
        books = list(collection.find().limit(10))
        return [book_helper(book) for book in books]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# 2. Retrieve a single book by ID
@app.get("/books/{book_id}", response_model=Book, tags=["Books"])
async def get_book(book_id: str):
    try:
        book = collection.find_one({"_id": ObjectId(book_id)})
        if book:
            return book_helper(book)
        raise HTTPException(status_code=404, detail="Book not found")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# 3. Add a new book
@app.post("/books/", response_model=Book, tags=["Books"])
async def add_book(new_book: BookCreate):
    try:
        # Convert Pydantic model to dictionary, removing any None values
        book_data = new_book.dict()
        result = collection.insert_one(book_data)
        
        # Retrieve the newly inserted book
        inserted_book = collection.find_one({"_id": result.inserted_id})
        return book_helper(inserted_book)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding book: {str(e)}")

# 4. Update a book
@app.put("/books/{book_id}", response_model=Book, tags=["Books"])
async def update_book(book_id: str, updated_data: BookUpdate):
    try:
        # Convert to ObjectId
        object_id = ObjectId(book_id)
        
        # Remove None values from update
        update_dict = {k: v for k, v in updated_data.dict().items() if v is not None}
        
        # Update the book
        result = collection.update_one(
            {'_id': object_id},
            {'$set': update_dict}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Book not found or no changes made")
        
        # Retrieve and return the updated book
        updated_book = collection.find_one({'_id': object_id})
        return book_helper(updated_book)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating book: {str(e)}")


# 5. Delete a book
@app.delete("/books/{book_id}", tags=["Books"])
async def delete_book(book_id: str):
    try:
        # Convert book_id to ObjectId
        object_id = ObjectId(book_id)
        
        # Delete the book
        result = collection.delete_one({'_id': object_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Book not found")
        
        return {"message": f"Book with ID {book_id} has been deleted successfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting book: {str(e)}")
