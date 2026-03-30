import streamlit as st
from supabase import create_client, Client


def get_supabase_client() -> Client:
    """Get a Supabase client using secrets from Streamlit or environment."""
    url = st.secrets.get("SUPABASE_URL", "")
    key = st.secrets.get("SUPABASE_KEY", "")
    if not url or not key:
        st.error("请配置 SUPABASE_URL 和 SUPABASE_KEY")
        st.stop()
    return create_client(url, key)
