"""
Homepage.py
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
import glob
import pandas as pd
import numpy as np
from datetime import datetime

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from ete3 import Tree, TreeStyle, PhyloTree, TextFace, NodeStyle, SeqMotifFace
# from ete3 import faces, AttrFace, CircleFace, TextFace, RectFace

st.set_page_config(page_title="Homepage", page_icon="🐨")

st.title("Koalafy - Tree Visualizer")
st.caption("Cohn Lab | Fred Hutchinson Cancer Center")
st.markdown("""**Koalafy** is a web-based phylogenetic tree visualization tool designed to help researchers
analyze and visualize evolutionary relationships in sequencing data""")
st.image("data/Three_koalas.jpg", caption="Image source: https://commons.wikimedia.org/wiki/File:Three_koalas.jpg")
st.markdown("""
\n Built by the Cohn Lab
at Fred Hutchinson Cancer Center, this tool automatically identifies clonal sequences
(sequences that are nearly identical) and collapses them into "stacked nodes" for clearer visualization...
""")

st.code("""
    🌿
    ├── 🐨
    │   ├── 🐨🐨
    │   └── 🐨
    └── 🐨🐨🐨
""")

st.markdown("""
**...Just like a bunch of stacked koalas hanging on a eucalyptus branch!**
""")

st.markdown("### Quick Start Guide")
with st.expander("🌿 Click to see Koalafy's workflow"):
    st.markdown("""
    Getting started with Koalafy is simple! You need just two things:

    1. **A tree file** - Newick format output from phylogenetic analysis tools (e.g., FigTree, IQ-TREE)
    2. **Node annotations** (optional) - Information about your sequence types for custom colors and shapes

    **Workflow:**
    1. Navigate to the Homepage
    2. Configure the Sequence Parser table with your sequence characteristics (optional)
    3. Upload your tree file in the "Tree File Upload" section
    4. View your visualization with default/custom settings
    5. Adjust visualization settings (optional)
    6. Download visualization as a SVG file
    """)

    st.info("**Privacy Note:** All data processing happens in real-time. Your tree files and sequences are NOT stored on our servers. Refreshing the page will clear all uploaded data.")

st.markdown("For more detailed instructions and examples, please reference the `About` page.")

# Upon start, search for uploaded_tree.tre in current dir, or tree-file.png/pdf in data/ and clear
def clear_files():
    """
    When this function is called, uploaded_tree.tre temp file is cleared from directory and
    any existing png/pdf/svg files in the data directory are also cleared
    """
    pdf_files = glob.glob(os.path.join('./data/', '**', '*.pdf'), recursive=True)
    for file in pdf_files:
        os.remove(file)
    png_files = glob.glob(os.path.join('./data/', '**', '*.png'), recursive=True)
    for file in png_files:
        os.remove(file)
    svg_files = glob.glob(os.path.join('./data/', '**', '*.svg'), recursive=True)
    for file in svg_files:
        os.remove(file)
    if os.path.isfile('uploaded_tree.tre'):
        os.remove('uploaded_tree.tre')

clear_files()

st.header("Sequence Parser")
tab1, tab2 = st.tabs(["Online Input", "CSV Upload"])
# defining parser
df = pd.DataFrame(
    [
        {"SeqType": "Type 1", "Parser": "", "Color": "#FFA600", "Shape": "Circle"},
        {"SeqType": "Type 2", "Parser": "", "Color": "#63BFCF", "Shape": "Circle"},
    ]
)
default_parser = df.copy()
with tab1:
    edited_df = st.data_editor(
        df,
        column_config={
            "SeqType": st.column_config.TextColumn(
                "Sequence Characteristic Label",
                help="Type of Sequence", required=True
            ),
            "Parser": st.column_config.TextColumn(
                "Parser String",
                help="String to separate sequence type from sequence name", required=True
            ),
            "Color": st.column_config.TextColumn(
                "Color",
                help="Hexadecimal color code", required=True
            ),
            "Shape": st.column_config.TextColumn(
                "Shape",
                help="Supported node shapes: Circle, Triangle, Square, Pentagon (Default=Circle)", required=True
            )
        },
        hide_index=True, num_rows="dynamic"
    )
    st.caption("Parser Table - Add or Delete Entries by Selecting Rows")

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
        df = pd.read_csv(parser_upload)
        df = df.astype(str)
        if edited_df.isnull().any().any():
            st.error("Missing values detected. Parser table should not contain any missing values. Please re-upload corrected file.")
        else:
            st.success("Parser file successfully loaded!")
            # show uploaded df
            edited_df = st.data_editor(
                df,
                hide_index=True, num_rows="dynamic"
            )
            st.caption("Parser Table - Add or Delete Entries by Selecting Rows")
        if edited_df.isnull().any().any():  # check again for any human edits
                    st.error("Missing values detected. Parser table should not contain any missing values.")

# Add Shape Data - classification
st.subheader("Binary Shape Classification")
# circle - default, square - set to parse
on = st.toggle("Multiple Shapes")
st.markdown("""
            Specify types of sequences to set as square or circle shaped nodes. Best used for binary type assignments. 
            """)
if on:
    shape_df = pd.DataFrame(
        [
            {"Classification": "Type 1", "Parser": "", "Shape": "Square"},
            {"Classification": "Type 2", "Parser": "Default (Do Not Edit)", "Shape": "Circle"}
        ]
    )
    edited_shape = st.data_editor(
        shape_df,
        column_config={
            "Classification": st.column_config.TextColumn(
                "Sequence Characteristic Label",
                help="Sequence characteristic classifications", required=True
            ),
            "Parser": st.column_config.TextColumn(
                "Parser String",
                help="String to separate square classification from circles", required=True
            ),
            "Shape": st.column_config.TextColumn(
                "Shape",
                help="Node Shape",
            )
        },
        disabled=["Shape"],
        hide_index=True, num_rows="fixed"
    )

# expander containing customisable settings
st.subheader("Tree Settings")
with st.expander("Tree Visualization Options"):
    # setting scale
    ts_scale_parameter = 10000 # default value
    scale_range = np.arange(1000, 11000, 1000).tolist()
    ts_scale = st.select_slider(
        "Set the branch length scale",
        options=scale_range,
        value=10000 # default value
        )
    if ts_scale != 10000:
        ts_scale_parameter = ts_scale

    # setting clone stacking threshold
    threshold = 1e-06 # set threshold to be ~1 mutation (double check)
    clone_range = [1e-08, 1e-07, 1e-06, 1e-05, 1e-04, 1e-03, 1e-02, 1e-01]
    threshold_slider = st.select_slider(
        "Set the clonality distance threshold \
            (higher values have higher threshold for clones)",
        options=clone_range,
        value=1e-06 # default value
        )
    if threshold_slider != 1e-06:
        threshold = threshold_slider

    # if turned on, then leaf names will show
    leaf_name_bool = False
    leaf_name_on = st.toggle("Show Node Name")
    if leaf_name_on:
        leaf_name_bool = True
        st.caption("Only the sequence name of the leading node is shown \
                   (collapsed clones are not named)")
        
    # set the rooting of the tree if you dont want midpoint rooting
    tree_root = st.text_input("Set Tree Outgroup Node Name", "Midpoint Rooting")
    if tree_root == 'Midpoint Rooting' or tree_root == '':
        tree_root = "midpoint"
    else:
        tree_root = str(tree_root)
    st.caption("Default behavior set to midpoint rooting if node name is not valid")

# dictionary of tree visualization settings (keyword arguments)
kwargs = {
    "ts_scale": ts_scale_parameter,
    "clone_threshold": threshold,
    "leaf_name_bool": leaf_name_bool,
    "rooting_node": tree_root
}
kwargs = pd.DataFrame([kwargs]) # convert to df
kwargs = kwargs.to_csv(index=False)

st.header("Tree File Upload")
# upload file
uploaded_file = st.file_uploader("Please upload your newick file", 
                                 type=["tre", "nwk", "tree", "newick", "nhx"],
                                 accept_multiple_files = False)

if uploaded_file:
    # Check that parser table is updated
    if edited_df.equals(default_parser):
        st.warning('Warning: seems like you have not updated the parser table. Results may be unexpected!', icon="⚠️")
    # creates a file in writing mode
    temp_filename = "uploaded_tree.tre"
    with open(temp_filename,'w+b') as f:
        # writes the tree to the file
        f.write(uploaded_file.getbuffer())

    # serializing df to csv
    df_csv = edited_df.to_csv(index=False)

    if on:
        class_csv = edited_shape.to_csv(index=False)
        # run tree-render-function.py and pass the temp tree file as an argument
        subprocess.run([f"{sys.executable}", "tree-render-function.py", temp_filename, df_csv, class_csv, kwargs])
    else:
        # run tree-render-function.py and pass the temp tree file as an argument
        subprocess.run([f"{sys.executable}", "tree-render-function.py", temp_filename, df_csv, kwargs])

    # display tree
    if os.path.exists("data/tree-file.png"):
        st.header("Tree Visualization")
        # st.image("data/tree-file.png")
        st.image("data/tree-file.svg", width=10000)
        # with open("data/tree-file.pdf", "rb") as file:
        #     today_date = datetime.now().strftime("%Y-%m-%d")
        #     download_filename = f"tree-{today_date}.pdf"
        #     st.download_button(label = "Download Tree File as a PDF", data = file, file_name = download_filename, mime="application/pdf")
        with open("data/tree-file.svg", "rb") as file:
            today_date = datetime.now().strftime("%Y-%m-%d")
            download_filename = f"tree-{today_date}.svg"
            st.download_button(label = "Download Tree as a SVG", data = file, file_name = download_filename, mime="image/svg+xml")
    else: 
        st.error("Error in creating tree. tree-file image not found.")

# Footer
st.markdown("---")
st.caption("Koalafy - Tree Visualizer v1.0 | Cohn Lab @ Fred Hutchinson Cancer Center | Last Updated: January 2026")