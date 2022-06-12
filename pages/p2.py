import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
import numpy as np

st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")

"""
# My first app
Here's our first attempt at using data to create a table:
"""



import streamlit as st
import pandas as pd
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})


arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)
# plt.plot(range(100),[x**1.5 for x in range(100)])
# plt.show()

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', f'{x * x:,.2f}')

st.line_chart([x**1.5 for x in range(100)])


df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option


# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)