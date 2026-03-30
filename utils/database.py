from datetime import date
from typing import Any

import streamlit as st
from utils.supabase_client import get_supabase_client


def fetch_books(user_id: str) -> list[dict[str, str | int]]:
    """Fetch all books for a user, merging books table and notes."""
    client = get_supabase_client()

    # Get books from books table (with author)
    books_resp = (
        client.table("books")
        .select("book_name, author")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    book_info: dict[str, str] = {}
    for b in books_resp.data:
        book_info[b["book_name"]] = b.get("author", "")

    # Get note counts
    notes_resp = (
        client.table("notes")
        .select("book_name")
        .eq("user_id", user_id)
        .execute()
    )
    book_counts: dict[str, int] = {}
    for note in notes_resp.data:
        name = note["book_name"]
        book_counts[name] = book_counts.get(name, 0) + 1

    # Merge: all books from books table + any books that only appear in notes
    all_book_names = set(book_info.keys()) | set(book_counts.keys())
    result: list[dict[str, str | int]] = []
    for name in all_book_names:
        result.append({
            "book_name": name,
            "author": book_info.get(name, ""),
            "count": book_counts.get(name, 0),
        })
    result.sort(key=lambda x: -int(x["count"]))
    return result


def create_book(user_id: str, book_name: str, author: str) -> bool:
    """Add a book to the user's bookshelf. Returns True on success."""
    try:
        client = get_supabase_client()
        client.table("books").insert(
            {
                "user_id": user_id,
                "book_name": book_name,
                "author": author,
            }
        ).execute()
        return True
    except Exception as e:
        err_msg = str(e)
        if "duplicate" in err_msg.lower() or "unique" in err_msg.lower():
            st.warning("这本书已经在书架上了")
        else:
            st.error(f"添加失败: {e}")
        return False


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


def fetch_notes_for_book(
    user_id: str, book_name: str, time_range: str | None = None
) -> list[dict[str, Any]]:
    """Fetch notes for a specific book, optionally filtered by time range.

    time_range: None (all), 'week', 'month', 'year'
    """
    client = get_supabase_client()
    query = (
        client.table("notes")
        .select("sentence, thought, date")
        .eq("user_id", user_id)
        .eq("book_name", book_name)
    )

    if time_range:
        from datetime import date as date_cls, timedelta
        today = date_cls.today()
        if time_range == "week":
            start = today - timedelta(days=7)
        elif time_range == "month":
            start = today - timedelta(days=30)
        elif time_range == "year":
            start = today - timedelta(days=365)
        else:
            start = None
        if start:
            query = query.gte("date", start.isoformat())

    response = query.order("date", desc=False).execute()
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
