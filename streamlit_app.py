"""Streamlit entry point for Docalypt."""

from __future__ import annotations

import streamlit as st

from docalypt.interfaces.streamlit.app import run


st.set_page_config(page_title="Docalypt", page_icon="📄", layout="wide")
run()
