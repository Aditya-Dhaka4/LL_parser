import streamlit as st
from parser_logic import parse, get_parsing_table
import pandas as pd

st.title("LL(1) Predictive Parser")
st.write("Grammar Used (After Left Factoring):")
st.code("""
S → iEtS X  
X → eS | ε  
E → b
""")

user_input = st.text_input("Enter input string (e.g., ibtibee):")

if user_input:
    st.subheader("Parsing Table")
    table = get_parsing_table()
    df = pd.DataFrame(columns=['i', 'b', 'e', '$'], index=['S', 'X', 'E'])
    for nt in table:
        for t in table[nt]:
            df.at[nt, t] = table[nt][t]
    st.dataframe(df.fillna(''))

    st.subheader("Parsing Steps")
    steps = parse(user_input)
    step_df = pd.DataFrame(steps)
    st.dataframe(step_df)
