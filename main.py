
from fastapi import FastAPI, HTTPException
from bson import ObjectId

from database import notes_collection
from models import Note

app = FastAPI(title="Notes Manager API")


# Convert MongoDB document into JSON-friendly data
def serialize_note(note):
    return {
        "id": str(note["_id"]),
        "title": note["title"],
        "content": note["content"]
    }


# Home API
@app.get("/")
def home():
    return {"message": "Welcome to Notes Manager API"}


# CREATE - Add a new note
@app.post("/notes")
def create_note(note: Note):

    note_data = note.model_dump()

    result = notes_collection.insert_one(note_data)

    saved_note = notes_collection.find_one(
        {"_id": result.inserted_id}
    )

    return {
        "message": "Note created successfully",
        "note": serialize_note(saved_note)
    }


# READ - Get all notes
@app.get("/notes")
def get_notes():

    notes = notes_collection.find()

    return [
        serialize_note(note)
        for note in notes
    ]


# READ - Get one note by ID
@app.get("/notes/{note_id}")
def get_note(note_id: str):

    if not ObjectId.is_valid(note_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid note ID"
        )

    note = notes_collection.find_one(
        {"_id": ObjectId(note_id)}
    )

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return serialize_note(note)


# UPDATE - Update a note
@app.put("/notes/{note_id}")
def update_note(note_id: str, note: Note):

    if not ObjectId.is_valid(note_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid note ID"
        )

    result = notes_collection.update_one(
        {"_id": ObjectId(note_id)},
        {"$set": note.model_dump()}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    updated_note = notes_collection.find_one(
        {"_id": ObjectId(note_id)}
    )

    return {
        "message": "Note updated successfully",
        "note": serialize_note(updated_note)
    }


# DELETE - Delete a note
@app.delete("/notes/{note_id}")
def delete_note(note_id: str):

    if not ObjectId.is_valid(note_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid note ID"
        )

    result = notes_collection.delete_one(
        {"_id": ObjectId(note_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return {
        "message": "Note deleted successfully"
    }
