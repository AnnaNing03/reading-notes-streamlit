import streamlit as st
from supabase import create_client, Client
def get_supabase_client() -> Client:
    """Get a Supabase client using secrets from Streamlit or environment.
    If the user is logged in, the client will carry their access token
    so that RLS policies (auth.uid()) work correctly.
    """
    url = st.secrets.get("SUPABASE_URL", "")
    key = st.secrets.get("SUPABASE_KEY", "")
    if not url or not key:
        st.error("请配置 SUPABASE_URL 和 SUPABASE_KEY")
        st.stop()
    client = create_client(url, key)
    # Attach the logged-in user's JWT so auth.uid() resolves in RLS
    access_token = st.session_state.get("access_token")
    if access_token:
        client.postgrest.auth(access_token)
    return client
