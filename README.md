# cohn-treemaker
WebApp to create Phylogenetic Trees from sequencing data newick files and stack clonal sequences.

This tool is made by the Cohn Lab at Fred Hutch. If you would like to use it, please reach out to use (wazam@fredhutch.org)

### How to Launch (Locally):

Please ensure you have streamlit installed and other necessary libraries (pandas, PyQT5, ETE3). Please check environment.yml & requirements.txt to check for all necessary libraries and versions!

Run `streamlit run 1_🐨_Homepage.py` from root of directory after cloning the github repo to locally launch dashboard.

## Cohn Treemaker Web Tool

### Overview

**Koalafy** is a web-based phylogenetic tree visualization tool designed to help researchers
analyze and visualize evolutionary relationships in sequencing data. 
\n Built by the Cohn Lab
at Fred Hutchinson Cancer Center, this tool automatically identifies clonal sequences
(sequences that are nearly identical) and collapses them into "stacked nodes" for clearer visualization...

**...Just like a bunch of stacked koalas hanging on a eucalyptus branch!**

**Key Features:**

- Automatic clone detection and visualization
- Custom color mapping for sequence types
- Multiple node shapes (circle, square, triangle, diamond, pentagon)
- Adjustable clonality threshold and tree scaling
- High-quality SVG image export for publications
- Data Privacy: no data is stored on the server

**How to Use**

Getting started with Koalafy is simple! You need just two things:

    1. A tree file- Newick format output from phylogenetic analysis tools (e.g., FigTree, IQ-TREE)
    2. Node annotations (optional) - Information about your sequence types for custom colors and shapes

**Workflow:**

    1. Navigate to the Homepage
    2. Configure the Sequence Parser table with your sequence characteristics (optional)
    3. Upload your tree file in the "Tree File Upload" section
    4. View your visualization with default/custom settings
    5. Adjust visualization settings (optional)
    6. Download visualization as a SVG file

**Parser Example**

For Example:
    
| Sequence Characteristic | Parser String | Color    | Shape    |
|------------------------|---------------|----------|----------|
| Wildtype               | WT            | #FFA600  | Circle   |
| Mutant Strain A        | MutA          | #63BFCF  | Triangle |
| Mutant Strain B        | MutB          | #FF6361  | Square   |

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
    
### Tree Upload

Upload your phylogenetic tree file in one of the supported Newick formats:

**Supported formats:** `.tre`, `.nwk`, `.newick`, `.tree`, `.nhx`

The tree will be automatically:

- Rooted at the midpoint (or custom outgroup if specified)
- Ladderized for better visualization
- Analyzed for clonal sequences based on branch length distances

### Clone Stacking

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

### Visualization Options

**Node Colors:** Node colors are determined by the hexadecimal color codes in your Sequence Parser table

**Node Shapes:** Five shapes are supported for node visualization (Circle, Square, Triangle, Diamond, Pentagon)

**Scale:** Adjust branch length display (1000-11000)

- Higher values = longer branches
- The scale bar updates automatically

**Clonality Threshold:** Set the distance threshold for grouping clones (1e-08 to 1e-01)

- Lower values = stricter definition of clones (must be more similar)
- Higher values = more sequences grouped together
- Default: 1e-06 (~1 mutation difference, though this changes by sequence length used to generate trees)

**Show Node Names:** Toggle to display sequence names for leading nodes

**Tree Outgroup:** Specify a custom root node name (default: midpoint rooting)

## Contact/Acknowledgements

**How to cite Koalafy:**

Koalafy Tree Visualizer. Cohn Lab, Fred Hutchinson Cancer Center (2025).
Available at: https://koalafytrees.fredhutch.org

For academic publications, please include the URL and acknowledgment of the Cohn Lab.

**Developed by:**
Cohn Lab, Fred Hutchinson Cancer Center

**Source Code:**
[github.com/walkerazam/cohn-treemaker](https://github.com/walkerazam/cohn-treemaker)

**Citations**:

1. Huerta-Cepas J, Serra F, Bork P. ETE 3: Reconstruction, Analysis, and Visualization of Phylogenomic Data. Mol Biol Evol. 2016 Jun;33(6):1635-8. doi: 10.1093/molbev/msw046. Epub 2016 Feb 26. PMID: 26921390; PMCID: PMC4868116.
2. Streamlit v1.43.0 (https://streamlit.io). Copyright 2026 Snowflake Inc

If you encounter any problems, have questions, or would like to use this tool for your research:

**Contact:** Walker Azam

**Email:** wazam@fredhutch.org

### Report Issues

Found a bug? Have a feature request? Please contact us via email with:

- A description of the issue
- Your browser and operating system
- Steps to reproduce (if applicable)
- Example files (if relevant)