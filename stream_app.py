from doctest import DocFileCase
import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
import numpy as np
import streamlit.components.v1 as components 

from blog_aggregator.utils import load_db

from PIL import Image


image = Image.open('blog_logos/OSAM.png')

st.image(image,'OSAM',width=200)


# df = load_db() 
# df

# st.markdown(lol,unsafe_allow_html=True)
# components.html(lol,width=1000,height=1500)

