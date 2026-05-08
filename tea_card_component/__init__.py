import os
import streamlit.components.v1 as components

_build_dir = os.path.join(os.path.dirname(__file__), "frontend", "build")

tea_card = components.declare_component(
    "tea_card",
    path=_build_dir
)