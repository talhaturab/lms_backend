from pymongo import MongoClient
from bson import ObjectId

# MongoDB connection setup
uri = "mongodb+srv://talhaturab:IiWHs4jBHbYuz6Jd@cluster0.likby.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
db_string = 'books_db'  # Database name
collection_string = 'books_collection'  # Collection name

# Utility function to convert MongoDB's ObjectId to string
def book_helper(book) -> dict:
    return {
        "_id": str(book["_id"]),
        "title": book["title"],
        "authors": book["authors"],
        "description": book["description"],
        "category": book["category"],
        "publisher": book["publisher"],
        "publish_date": book["publish_date"],
        "price": book["price"],
        "quantity_available": book["quantity_available"]
    }