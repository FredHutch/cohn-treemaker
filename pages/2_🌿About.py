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

st.markdown("""
### Overview

**Koalafy** is a web-based phylogenetic tree visualization tool designed to help researchers
analyze and visualize evolutionary relationships in sequencing data. 
\n Built by the Cohn Lab
at Fred Hutchinson Cancer Center, this tool automatically identifies clonal sequences
(sequences that are nearly identical) and collapses them into "stacked nodes" for clearer visualization...
""")

st.markdown("""
**...Just like a bunch of stacked koalas hanging on a eucalyptus branch!**

\n #### This page contains more details and examples of how to use this tool
""")

st.image("data/KoalafyExample.jpg", caption="Example of Koalafying your Tree!")

st.markdown("""
**Key Features:**
- 🐨 Automatic clone detection and visualization
- 🎨 Custom color mapping for sequence types
- 🔷 Multiple node shapes (circle, square, triangle, diamond, pentagon)
- 🌿 Adjustable clonality threshold and tree scaling
- 📊 High-quality SVG image export for publications
- 🔒 Data Privacy: no data is stored on the server
""")

st.info("**Privacy Note:** All data processing happens in real-time. Your tree files and sequences are NOT stored on our servers. Refreshing the page will clear all uploaded data.")

# Divider
st.markdown("---")

# Quick Start Section
st.markdown("## Quick Start Guide")

st.markdown("""
Getting started with Koalafy is simple! You need just two things:

1. **A tree file** - Newick format output from phylogenetic analysis tools (e.g., FigTree, IQ-TREE)
2. **Node annotations** (optional) - Information about your sequence types for custom colors and shapes

**Minimum workflow:**
1. Navigate to the Homepage
2. Upload your tree file in the "Tree File Upload" section
3. View your visualization with default settings
4. Download as SVG

**For custom visualizations:**
1. Configure the Sequence Parser table with your sequence characteristics
2. Upload your tree file
3. Adjust visualization settings (optional)
4. Download your customized tree
""")

# Divider
st.markdown("---")

# Detailed Instructions
st.markdown("## Detailed Instructions")

# Step 1
st.markdown("### Step 1: Configure the Sequence Parser")

st.markdown("""
The **Sequence Parser** tells Koalafy how to identify and style different types of sequences in your tree.
You can configure it directly on the webpage or upload a CSV file with your parser settings.

**What you need to provide:**
- **Sequence Characteristic Label**: A descriptive name for this sequence type (e.g., "Rebound", "Wildtype")
- **Parser String**: A unique text pattern found in sequence names that identifies this type
- **Color**: Hexadecimal color code for this sequence type (e.g., #FFA600)
- **Shape**: Node shape for visualization (Circle, Square, Triangle, Diamond, Pentagon)
""")

st.markdown("**Example Parser Table:**")
st.markdown("""
| Sequence Characteristic | Parser String | Color    | Shape    |
|------------------------|---------------|----------|----------|
| Wildtype               | WT            | #FFA600  | Circle   |
| Mutant Strain A        | MutA          | #63BFCF  | Triangle |
| Mutant Strain B        | MutB          | #FF6361  | Square   |
""")

with st.expander("🔍 Click to see how parser strings work"):
    st.markdown("""
    The parser string is matched against your sequence names in the Newick file. For example:

    - Sequence name: `sample_WT_clone_001` → Node name contains "WT" → Colored #FFA600 (orange) with Circle shape
    - Sequence name: `patient_5_MutA_replicate_2` → Node name contains "MutA" → Colored #63BFCF (blue) with Triangle shape
    - Sequence name: `control_MutB_day7` → Node name contains "MutB" → Colored #FF6361 (red) with Square shape

    **Important:** Parser strings are case-sensitive and should be unique to avoid conflicts.
                
    **Limitation**: Due to technical constraints, you cannot assign two different shapes
    to sequences with identical colors using the main parser table alone. Often changing the last
    character in the color code to an adjacent character circumvents this problem and is generally
    not visibly distinguishable (e.g., #63BFCF with Triangle shape vs #63BFCG with Square shape)

    **What happens to unmapped sequences?**
    Sequences that don't match any parser string will appear as black circles and be labeled
    "Undefined Sequence" in the legend.
    """)

st.markdown("""
**Two ways to configure the parser:**
1. **Online Input Tab**: Manually enter your parser settings in the interactive table
2. **CSV Upload Tab**: Upload a pre-configured parser CSV file (download template below)
""")

# Step 2
st.markdown("### Step 2: Upload Your Tree File")

st.markdown("""
Upload your phylogenetic tree file in one of the supported Newick formats:

**Supported formats:** `.tre`, `.nwk`, `.newick`, `.tree`, `.nhx`

The tree will be automatically:
- Rooted at the midpoint (or custom outgroup if specified)
- Ladderized for better visualization
- Analyzed for clonal sequences based on branch length distances
""")

# Step 3
st.markdown("### Step 3: Customize Visualization Settings (Optional)")

st.markdown("""
Fine-tune your tree visualization using the **Tree Settings** section:

**Scale:** Adjust branch length display (1000-11000)
- Higher values = longer branches
- The scale bar updates automatically

**Clonality Threshold:** Set the distance threshold for grouping clones (1e-08 to 1e-01)
- Lower values = stricter definition of clones (must be more similar)
- Higher values = more sequences grouped together
- Default: 1e-06 (~1 mutation difference, though this changes by sequence length used to generate trees)

**Show Node Names:** Toggle to display sequence names for leading nodes

**Tree Outgroup:** Specify a custom root node name (default: midpoint rooting)
""")

with st.expander("🔷 Binary Shape Classification"):
    st.markdown("""
    In addition to the main parser table, you can use **Binary Shape Classification** to
    distinguish between two types of sequences using only Circle vs. Square shapes.

    This is useful when you have a secondary binary classification (e.g., intact vs. defective sequences)
    that overlays your primary color classification.

    **Example use case:**
    - Primary classification (colors): Different viral strains
    - Secondary classification (shapes): Intact genomes (circles) vs. defective genomes (squares)

    **Note:** This feature works independently of the shape column in the main parser table.
    """)

# Step 4
st.markdown("### Step 4: Download Your Visualization")

st.markdown("""
Once your tree is rendered, you can download it as a high-quality **SVG file**
(Scalable Vector Graphics) for use in publications, presentations, or further editing
in vector graphics software (Adobe Illustrator/InkScape/etc...)

The downloaded file will be named with the current date: `tree-YYYY-MM-DD.svg`
""")

# Divider
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Node Colors")
    st.markdown("""
    Node colors are determined by the hexadecimal color codes in your Sequence Parser table.

    **Tips for choosing colors:**
    - Use high contrast colors for better visibility
    - Consider colorblind-friendly palettes
    - You can also [passed named colors from Python](https://matplotlib.org/stable/gallery/color/named_colors.html) directly instead of the hexadecimal color code.
    """)

with col2:
    st.markdown("### Node Shapes")
    st.markdown("""
    Five shapes are supported for node visualization:
    - **Circle** (default)
    - **Square**
    - **Triangle**
    - **Diamond**
    - **Pentagon**

    Shapes are mapped to colors via the parser table.
    """)

st.markdown("### Clone Stacking")
st.markdown("""
The key feature of Koalafy is automatic clone detection and stacking. When multiple sequences
are within the clonality threshold distance of each other and share the same sequence type,
they are collapsed into a single node with stacked symbols representing each clone.

**How it works:**
1. The tool calculates pairwise distances between all leaf nodes
2. Sequences within the threshold distance are identified as clones
3. Clones of the same type are visually stacked at a single node
4. Different sequence types can also be stacked together if they're clonal

The leading node (first sequence in each clone group) is kept, and its name is shown
if "Show Node Names" is enabled.
""")

# Divider
st.markdown("---")

# Template and Resources
st.markdown("## Template & Resources")

st.markdown("### Download Parser Template")
st.markdown("Use this CSV template to prepare your parser settings offline:")

try:
    with open("data/parser-template.csv", "rb") as file:
        st.download_button(
            label="📥 Download Template Parser CSV",
            data=file,
            file_name="parser-template.csv",
            mime="application/csv"
        )
    st.caption("You can also download this template from the 'CSV Upload' tab on the Homepage.")
except FileNotFoundError:
    st.warning("Parser template file not found. Please download from the Homepage.")

# Divider
st.markdown("---")

# Troubleshooting
st.markdown("## Troubleshooting & FAQ")

with st.expander("❓ My tree isn't rendering. What should I check?"):
    st.markdown("""
    1. **File format**: Ensure your file has one of these extensions: `.tre`, `.nwk`, `.newick`, `.tree`, `.nhx`
    2. **Valid Newick format**: Check that your tree file is properly formatted
    3. **Parser table**: Make sure there are no empty cells in the parser table
    4. **File size**: Very large trees may take longer to process
    5. **Try default settings**: Upload without customizing the parser first to isolate the issue
    """)

with st.expander("❓ What clonality threshold should I use?"):
    st.markdown("""
    The default value of **1e-06** works well for most cases (approximately 1 nucleotide substitution).

    - **For stricter clone grouping**: Use lower values (1e-07, 1e-08)
    - **For more permissive grouping**: Use higher values (1e-05, 1e-04)
    - **Depends on your data**: Branch lengths vary by analysis method and evolutionary distance

    Tip: Try different thresholds and compare results!
    """)

with st.expander("❓ Can I use this tool for publications?"):
    st.markdown("""
    Yes! The SVG output is publication-quality and can be further edited in vector graphics software.

    Please cite the tool as:
    ```
    Koalafy Tree Visualizer. Cohn Lab, Fred Hutchinson Cancer Center (2025).
    Available at: https://koalafytrees.fredhutch.org
    ```
    """)

with st.expander("❓ What's the difference between the shape options?"):
    st.markdown("""
    There are two ways to assign shapes:

    1. **Main Parser Table - Shape Column**: Maps shapes to specific colors/sequence types.
       All nodes of that sequence type will have that shape. Supports all 5 shapes.

    2. **Binary Shape Classification Toggle**: Creates a secondary layer of classification
       using only Circles vs. Squares based on a parser string. Useful for overlaying a
       binary characteristic (like intact/defective) on top of your primary classification.

    **Limitation**: Due to technical constraints, you cannot assign two different shapes
    to sequences with identical colors using the main parser table alone.
    """)

with st.expander("❓ How many sequences can Koalafy handle?"):
    st.markdown("""
    The tool can handle trees with hundreds of sequences. Very large trees (>1000 sequences)
    may take longer to process and render. If you experience performance issues with very
    large datasets, consider:

    - Simplifying your tree by removing distant outgroups
    - Increasing the clonality threshold to collapse more nodes
    - Processing subsets of your data separately
    """)

with st.expander("❓ Why isn't my custom outgroup working?"):
    st.markdown("""
    Make sure:
    1. The node name exactly matches a sequence name in your tree (case-sensitive)
    2. There are no extra spaces in the node name
    3. The sequence exists in your uploaded tree file

    If the specified outgroup is invalid, the tool will automatically fall back to midpoint rooting.
    """)

# Divider
st.markdown("---")

# Technical Details (for advanced users)
with st.expander("🔧 Technical Details (Advanced)"):
    st.markdown("""
    ### Implementation Details

    **Clone Detection Algorithm:**
    - Pairwise distance calculation using ETE3 toolkit
    - Sequences within threshold distance are grouped
    - Weight assignment for visualization (number of collapsed sequences)
    - Preserves branch lengths during pruning

    **Tree Processing:**
    - Automatic midpoint rooting (or custom outgroup)
    - Ladderization for improved readability
    - Branch length preservation

    **Visualization Engine:**
    - Built with ETE3 (Evolution Tools Environment)
    - SVG post-processing for shape customization using lxml
    - Custom layout functions for clone stacking

    **Supported Newick Variants:**
    - Standard Newick format
    - Extended Newick (NHX) with annotations
    - Branch lengths required for clone detection

    ### Dependencies
    - Python 3.12
    - Streamlit (web interface)
    - ETE3 (tree manipulation and rendering)
    - PyQt5 (rendering backend)
    - pandas, numpy (data processing)
    - lxml (SVG manipulation)
    """)

# Divider
st.markdown("---")

# Citation Section
st.markdown("## Citation & Acknowledgments")

st.success("""
**How to cite Koalafy:**

Koalafy Tree Visualizer. Cohn Lab, Fred Hutchinson Cancer Center (2025).
Available at: https://koalafytrees.fredhutch.org

For academic publications, please include the URL and acknowledgment of the Cohn Lab.
""")

st.markdown("""
**Developed by:**
Cohn Lab, Fred Hutchinson Cancer Center

**Source Code:**
[github.com/walkerazam/cohn-treemaker](https://github.com/walkerazam/cohn-treemaker)
""")

# Divider
st.markdown("---")

# Contact and Support
st.markdown("## Get Help & Contact")

st.markdown("""
### Need Assistance?

If you encounter any problems, have questions, or would like to use this tool for your research:

**Contact:** Walker Azam
**Email:** wazam@fredhutch.org

**Before reaching out, please check:**
1. The Troubleshooting & FAQ section above
2. That your file format is supported
3. That your parser table has no empty values or errors/typos

### Request Access

This tool is made available by the Cohn Lab at Fred Hutch. If you would like to use it
for your research, please reach out to the contact above.

### Report Issues

Found a bug? Have a feature request? Please contact us via email with:
- A description of the issue
- Your browser and operating system
- Steps to reproduce (if applicable)
- Example files (if relevant)
""")

# Footer
st.markdown("---")
st.caption("Koalafy - Tree Visualizer v1.0 | Cohn Lab @ Fred Hutchinson Cancer Center | Last Updated: January 2025")