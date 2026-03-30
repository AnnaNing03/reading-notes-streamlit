from datetime import date
from typing import Any

import streamlit as st
from utils.supabase_client import get_supabase_client


def fetch_books(user_id: str) -> list[dict[str, str | int]]:
    """Fetch distinct books with note counts for a user."""
    client = get_supabase_client()
    response = (
        client.table("notes")
        .select("book_name")
        .eq("user_id", user_id)
        .execute()
    )
    book_counts: dict[str, int] = {}
    for note in response.data:
        name = note["book_name"]
        book_counts[name] = book_counts.get(name, 0) + 1
    result: list[dict[str, str | int]] = [
        {"book_name": name, "count": count}
        for name, count in sorted(book_counts.items(), key=lambda x: -x[1])
    ]
    return result


def fetch_notes(user_id: str, book_name: str | None = None) -> list[dict[str, Any]]:
    """Fetch notes for a user, optionally filtered by book name."""
    client = get_supabase_client()
    query = client.table("notes").select("*").eq("user_id", user_id)
    if book_name:
        query = query.eq("book_name", book_name)
    query = query.order("date", desc=True)
    response = query.execute()
    return response.data


def fetch_note_by_id(note_id: str, user_id: str) -> dict[str, Any] | None:
    """Fetch a single note by ID."""
    client = get_supabase_client()
    response = (
        client.table("notes")
        .select("*")
        .eq("id", note_id)
        .eq("user_id", user_id)
        .execute()
    )
    if response.data:
        return response.data[0]
    return None


def create_note(
    user_id: str,
    book_name: str,
    sentence: str,
    thought: str,
    note_date: date,
) -> bool:
    """Create a new note. Returns True on success."""
    try:
        client = get_supabase_client()
        client.table("notes").insert(
            {
                "user_id": user_id,
                "book_name": book_name,
                "sentence": sentence,
                "thought": thought,
                "date": note_date.isoformat(),
            }
        ).execute()
        return True
    except Exception as e:
        st.error(f"保存失败: {e}")
        return False


def delete_note(note_id: str, user_id: str) -> bool:
    """Delete a note. Returns True on success."""
    try:
        client = get_supabase_client()
        client.table("notes").delete().eq("id", note_id).eq(
            "user_id", user_id
        ).execute()
        return True
    except Exception as e:
        st.error(f"删除失败: {e}")
        return False


def fetch_notes_for_book(user_id: str, book_name: str) -> list[dict[str, Any]]:
    """Fetch all notes for a specific book."""
    client = get_supabase_client()
    response = (
        client.table("notes")
        .select("sentence, thought, date")
        .eq("user_id", user_id)
        .eq("book_name", book_name)
        .order("date", desc=False)
        .execute()
    )
    return response.data


def fetch_years(user_id: str) -> list[str]:
    """Fetch distinct years from user's notes."""
    client = get_supabase_client()
    response = (
        client.table("notes").select("date").eq("user_id", user_id).execute()
    )
    years: set[str] = set()
    for note in response.data:
        if note.get("date"):
            years.add(note["date"][:4])
    return sorted(years, reverse=True)


def fetch_books_for_year(
    user_id: str, year: str
) -> list[dict[str, str | int]]:
    """Fetch books and note counts for a specific year."""
    client = get_supabase_client()
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    response = (
        client.table("notes")
        .select("book_name")
        .eq("user_id", user_id)
        .gte("date", start_date)
        .lte("date", end_date)
        .execute()
    )
    book_counts: dict[str, int] = {}
    for note in response.data:
        name = note["book_name"]
        book_counts[name] = book_counts.get(name, 0) + 1
    result: list[dict[str, str | int]] = [
        {"book_name": name, "count": count}
        for name, count in sorted(book_counts.items(), key=lambda x: -x[1])
    ]
    return result
