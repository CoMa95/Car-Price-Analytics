# import libraries
from pathlib import Path
import textwrap
from typing import Dict, List
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# ---------------- Page config ----------------
st.title("Western Car Price System Analysis")
st.caption("This dashboard provides insights into Western car prices through "
           "filtering, summarizing, visualization, and price prediction. "
           "Built with Streamlit + pandas + matplotlib.")

df = st.session_state['df']
