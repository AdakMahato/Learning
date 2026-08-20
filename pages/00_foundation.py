import streamlit as st
from story_data import STORIES
from level_content import LEVEL_CONTENT
from ui import render_episodic_page

story_id = 0
story = next(s for s in STORIES if s["id"] == story_id)
data = LEVEL_CONTENT.get(story_id, {"episodes": []})

render_episodic_page(story_id, story, data)
