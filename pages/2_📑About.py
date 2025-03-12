"""
2_📑_About.py
    Secondary About page containing description
    of the web app and other information.
    For more information see:
    https://github.com/walkerazam/cohn-treemaker
"""
import streamlit as st
import subprocess
import sys
import os

st.title("About Page")

st.markdown("## How to Use")
st.markdown("""
    To begin, please update the parser dataframe to fit the type of sequences you will be working with. 
    For each given sequence type, include a string parser that is included in the sequence name which differentiates 
    it from other sequence types. Provide a color hexademical to be associated with the given sequence type. 
            
    For Example:
    
    | Sequence Characteristic    | Parser String | Color |
    | -------- | ------- | ------- |
    | Rebound  | RBD   |  #FFA600 |  
    | Autologous IgG Outgrowth  | AUB   |  #63BFCF |      
    """)
st.markdown("""   
    Here the parser string "RBD" can identify sequences that belong to the Sequence Type "Rebound".
    However if the sequence name instead contains "AUB", then it will be classified as a
    "Autologous IgG Outgrowth" Sequence Type. For each sequence type, as associated color is used for
    visualization.
    For repeated use of a saved parser, you can also upload a CSV containing the information too using the
    'CSV Upload' tab. Once you fill out the table, you can also save that as a CSV for future re-uploads.
            
    Once the parser table is updated correctly, please upload your newick file containing these sequences.
    Accepted newick file formats are .tre, .nwk, .newick, and .tree.  
    The resulting tree will be shown below. The resulting tree visualization can be downloaded as a PDF. 
    """)

st.markdown("## Template Parser CSV")
st.markdown("Below is a template csv to save custom parser settings for upload")
st.download_button(label = "Download Template Parser CSV", data = "data/parser-template.csv", file_name = "parser-template.csv", mime="application/csv")
st.markdown("Users can also download the parser template from the `Online Input` option in the mainpage.")