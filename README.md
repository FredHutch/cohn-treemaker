# cohn-treemaker
WebApp to create Phylogenetic Trees from sequencing data newick files and stack clonal sequences.

This tool is made by the Cohn Lab at Fred Hutch. If you would like to use it, please reach out to use (wazam@fredhutch.org)

### How to Launch (Locally):

Please ensure you have streamlit installed and other necessary libraries (pandas, PyQT5, ETE3). Please check environment.yml & requirements.txt to check for all necessary libraries and versions!

Run `streamlit run 1_🐨_Homepage.py` from root of directory after cloning the github repo to locally launch dashboard.

## Cohn Treemaker Web Tool

This tool creates phylogenetic tree visualizations from sequencing data. It searches for clonal sequences and collapses them into stacked nodes for visualizations automatically. 

**How to Use**

To begin, please update the parser dataframe to fit the type of sequences you will be working with. For repeated use of a saved parser, you can also upload a CSV containing the information too using the CSV Upload tab.

A 'parser' is what can be used to determine sequence characteristics from your tree's nodes. They should be identifiable characters within the sequence's name in the newick file you upload.

Once the parser table is updated correctly, please upload your newick file containing these sequences. The resulting tree will be shown below. If you would like, you can download the visualization as a PDF.

**Parser Example**

For Example:
    
| Sequence Characteristic    | Parser String | Color |
| -------- | ------- | ------- |
| Rebound  | RBD   |  #FFA600 |  
| Autologous IgG Outgrowth  | AUB   |  #63BFCF |

Here the parser string "RBD" can identify sequences that belong to the Sequence Type "Rebound".
However if the sequence name instead contains "AUB", then it will be classified as a
"Autologous IgG Outgrowth" Sequence Type. For each sequence type, as associated color is used for
visualization.
For repeated use of a saved parser, you can also upload a CSV containing the information too using the
'CSV Upload' tab. Once you fill out the table, you can also save that as a CSV for future re-uploads.

### Visualization Options

**Node Colors**

Colors for sequence types/characteristics are determined from the associated hexadecimal color code provided in the Sequence Parser table.

**Node Shape**

Currently there are two primary node shapes supported (circles and squares). Circle node shapes are default, however squares can be mapped to a specific sequence characteristic from the Shape Classification parser table. 

Similar to the main parser table, a parser string can be associated with Squares, while rest will be assigned Circle (default). For legend labelling, they can also be assigned labels within the table.

**Tree Settings**

In addition to color and shape, you can also manually change tree scale and clone stacking thresholds.

For *scale* the slider can adjust the branch lengths. The tree will update the scale bar to reflect the new scale.

For *clonality* the slider can be used determine the distance threshold used to group together 'clones'. A larger threshold means more nodes will be collapsed together.

Additionally the leading node name for each branch can be visualized. This is useful to double check what sequences are being collapsed. 