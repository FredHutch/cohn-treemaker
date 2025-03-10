"""
TreemakerHomepage.py
    This is the main landing page of the Treemaker Web App.
    It accepts the tree file from the user and the parser
    dataframe.
    This file passes the files to tree-render-functions.py
    which is run to generate the tree ans presents the 
    saved png.
    It then offers the user a choice to download the generated tree
    file.
    For more information see:
    https://github.com/walkerazam/cohn-treemaker
"""
import streamlit as st
import subprocess
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

from ete3 import Tree, TreeStyle, PhyloTree, TextFace, NodeStyle, SeqMotifFace
from ete3 import faces, AttrFace, CircleFace, TextFace, RectFace

st.title("Cohn Treemaker Web Tool")

st.markdown("This tool creates phylogenetic trees from sequencing data. It searches for clonal sequences and collapses them into stacked nodes for visualizations automatically.")
st.markdown("""
    To begin, please update the parser dataframe to fit the type of sequences you will be working with.
    For repeated use of a saved parser, you can also upload a CSV containing the information too using the
    CSV Upload tab.
            
    Once the parser table is updated correctly, please upload your newick file containing these sequences. 
    The resulting tree will be shown below. If you would like, you can download the visualization as a PDF. 
    """)

# To Do: upon start, search for uploaded_tree.tre in current dir, or tree-file.* in data/ and clear

st.header("Sequence Parser")
tab1, tab2 = st.tabs(["Online Input", "CSV Upload"])
# defining parser
df = pd.DataFrame(
    [
        {"SeqType": "Rebound", "Parser": "22", "Color": "#FFA600"},
        {"SeqType": "Control IgG Outgrowth", "Parser": "UDB", "Color": "#63BFCF"},
        {"SeqType": "Autologous IgG Outgrowth", "Parser": "AUB", "Color": "#DC3F93"},
        {"SeqType": "No IgG Outgrowth", "Parser": "STB", "Color": "#2B488C"}
    ]
)
with tab1:
    edited_df = st.data_editor(
        df,
        column_config={
            "SeqType": st.column_config.TextColumn(
                "Sequence Type",
                help="Type of Sequence",
            ),
            "Parser": st.column_config.TextColumn(
                "Parser String",
                help="String to separate sequence type from sequence name",
            ),
            "Color": st.column_config.TextColumn(
                "Color",
                help="Hexadecimal color code",
            )
        },
        hide_index=True, num_rows="dynamic"
    )
    st.caption("Parser Table")

    if edited_df.isnull().any().any():
        st.error("Parser table should not contain any missing values!")

with tab2:
    st.markdown("""You can upload your custom parser as CSV. Please ensure correct column headers and
                no missing values are present. To download template for the CSV, check
                the 'About Page'. """)
    # Option to upload CSV
    # upload file
    parser_upload = st.file_uploader("Upload Parser as CSV:", 
                                    type=["csv"],
                                    accept_multiple_files = False)
    st.caption("Parser Upload")
    # read in uploaded parser
    if parser_upload:
        edited_df = pd.read_csv(parser_upload)
        if edited_df.isnull().any().any():
            st.error("Missing values detected. Parser table should not contain any missing values. Please re-upload corrected file.")
        else:
            st.success("Parser file successfully loaded!")

# Add Shape Data


st.header("Tree Upload")
# upload file
uploaded_file = st.file_uploader("Please upload your newick file", 
                                 type=["tre", "nwk", "tree", "newick", "nhx"],
                                 accept_multiple_files = False)

if uploaded_file:
    # creates a file in writing mode
    temp_filename = "uploaded_tree.tre"
    with open(temp_filename,'w+b') as f:
        # writes the tree to the file
        f.write(uploaded_file.getbuffer())

    # serializing df to csv
    df_csv = edited_df.to_csv(index=False)

    # run tree-render-function.py and pass the temp tree file as an argument
    subprocess.run([f"{sys.executable}", "tree-render-function.py", temp_filename, df_csv], check=True)

    # display tree
    if os.path.exists("data/tree-file.png"):
        st.header("Tree Visualization")
        st.image("data/tree-file.png")
        with open("data/tree-file.pdf", "rb") as file:
            today_date = datetime.now().strftime("%Y-%m-%d")
            download_filename = f"tree-{today_date}.pdf"
            st.download_button(label = "Download Tree File as a PDF", data = file, file_name = download_filename, mime="application/pdf")
    else: 
        st.error("Error in creatng tree. tree-file.png not found.")

