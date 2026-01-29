"""
2_🌿_About.py
    Secondary About page containing description
    of the web app and other information.
    For more information see:
    https://github.com/walkerazam/cohn-treemaker
"""
import streamlit as st
import subprocess
import sys
import os
st.set_page_config(page_title="About", page_icon="🌿")
st.title("About Koalafy")

st.markdown("## How to Use")
st.markdown("""
    To begin, please update the parser dataframe to fit the type of sequences you will be working with. 
    For each given sequence type, include a string parser that is included in the sequence name which differentiates 
    it from other sequence types. Provide a color hexademical to be associated with the given sequence type. 
            
    For Example:
    
    | Sequence Characteristic    | Parser String | Color | Shape |
    | -------- | ------- | ------- | ------- |
    | Rebound  | RBD   |  #FFA600 |  Circle |
    | Autologous IgG Outgrowth  | AUB   |  #63BFCF | Circle |
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
    The resulting tree will be shown and can be downloaded as a PDF. 
    """)

st.markdown("""
### Visualization Options

**Node Colors**

Colors for sequence types/characteristics are determined from the associated hexadecimal color code provided in the Sequence Parser table.

**Node Shape**

Currently there are 5 primary node shapes supported (circle, square, triangle, diamond, pentagon). Circle node shapes are default. 
            Shapes to mapped to specific colors by hexadeximal matching. Identical colors currently cannot match to two distinct shapes
            other than using a binary circle and square differentiatior through a parser table as described below:

Similar to the main parser table, a parser string can be associated with Squares, while rest will be assigned Circle (default).
             For legend labelling, they can also be assigned labels within the table.

**Tree Settings**

In addition to color and shape, you can also manually change tree scale and clone stacking thresholds.

For *scale* the slider can adjust the branch lengths. The tree will update the scale bar to reflect the new scale.

For *clonality* the slider can be used determine the distance threshold used to group together 'clones'. 
            A larger threshold means more nodes will be collapsed together.

Additionally the leading node name for each branch can be visualized. This is useful to double check what sequences are being collapsed. 
""")

st.markdown("## Template Parser CSV")
st.markdown("Below is a template csv to save custom parser settings for upload")
with open("data/parser-template.csv", "rb") as file:
    st.download_button(label = "Download Template Parser CSV", data = file, file_name = "parser-template.csv", mime="application/csv")
st.markdown("Users can also download the parser template from the `Online Input` option in the mainpage.")

st.subheader("Citation")
st.markdown("""Please cite this tool if you use its visualizations by linking the URL (https://koalafytrees.fredhutch.org) and the Cohn Lab at Fred Hutch (2025)""")

st.subheader("Get Help")
st.markdown("""If you run into any problems, please reach out to me (wazam@fredhutch.org) for support!""")