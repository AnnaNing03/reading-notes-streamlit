import streamlit as st
from utils.supabase_client import get_supabase_client


def check_auth() -> bool:
    """Check if user is authenticated. Returns True if logged in."""
    return st.session_state.get("user") is not None


def get_user_id() -> str:
    """Get current user's ID."""
    user = st.session_state.get("user")
    if user is None:
        return ""
    return user.id


def get_user_email() -> str:
    """Get current user's email."""
    user = st.session_state.get("user")
    if user is None:
        return ""
    return user.email or ""


def login(email: str, password: str) -> tuple[bool, str]:
    """Login with email and password. Returns (success, error_message)."""
    try:
        client = get_supabase_client()
        response = client.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        st.session_state["user"] = response.user
        st.session_state["access_token"] = response.session.access_token
        return True, ""
    except Exception as e:
        return False, str(e)


def register(email: str, password: str) -> tuple[bool, str]:
    """Register with email and password. Returns (success, error_message)."""
    try:
        client = get_supabase_client()
        response = client.auth.sign_up({"email": email, "password": password})
        if response.user is not None:
            st.session_state["user"] = response.user
            if response.session is not None:
                st.session_state["access_token"] = response.session.access_token
            return True, ""
        return False, "注册失败，请稍后重试"
    except Exception as e:
        return False, str(e)


def logout() -> None:
    """Logout current user."""
    try:
        client = get_supabase_client()
        client.auth.sign_out()
    except Exception:
        pass
    st.session_state.pop("user", None)
    st.session_state.pop("access_token", None)
