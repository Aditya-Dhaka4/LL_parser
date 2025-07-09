import streamlit as st
import pandas as pd
from parser_logic import parse
from parsing_table_builder import get_first_follow_and_table

st.title("LL(1) Predictive Parser")
st.write("Grammar Used (After Left Factoring):")
st.code("""
S → iEtS S' | a
S' → eS | ε  
E → b
""")

user_input = st.text_input("Enter input string (e.g., ibtibea):")

if user_input:
    # 🔍 Compute first, follow, and parsing table dynamically
    first, follow, parsing_table = get_first_follow_and_table()

    # 🔠 FIRST Sets
    st.subheader("FIRST Sets")
    first_df = pd.DataFrame.from_dict(
        {nt: ', '.join(sorted(v)) for nt, v in first.items()},
        orient='index',
        columns=['FIRST']
    )
    st.dataframe(first_df)

    # 🔠 FOLLOW Sets
    st.subheader("FOLLOW Sets")
    follow_df = pd.DataFrame.from_dict(
        {nt: ', '.join(sorted(v)) for nt, v in follow.items()},
        orient='index',
        columns=['FOLLOW']
    )
    st.dataframe(follow_df)

    # 📋 Parsing Table
    st.subheader("Parsing Table")
    all_terminals = sorted({term for row in parsing_table.values() for term in row})
    table_df = pd.DataFrame(columns=all_terminals, index=parsing_table.keys())
    for nt in parsing_table:
        for terminal in parsing_table[nt]:
            prod = parsing_table[nt][terminal]
            table_df.at[nt, terminal] = f"{nt} → {' '.join(prod) if prod else 'ε'}"
    st.dataframe(table_df.fillna(""))

    # ▶️ Parsing Steps
    st.subheader("Parsing Steps")
    steps = parse(user_input)
    step_df = pd.DataFrame(steps)
    st.dataframe(step_df)
