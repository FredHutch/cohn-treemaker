# cohn-treemaker
WebApp to create Phylogenetic Trees from sequencing data newick files

## Cohn Treemaker Web Tool

This tool creates phylogenetic trees from sequencing data. It searches for clonal sequences and collapses them into stacked nodes for visualizations automatically. 

To begin, please update the parser dataframe to fit the type of sequences you will be working with. For each given sequence type, include a string parser that is included in the sequence name which differentiates it from other sequence types. Provide a color hexademical to be associated with the given sequence type.

*For example: Sequence Type = Rebound, Parser String = rbd, Color = #FFA600. Here the parser string "rbd" can identify sequences that belong to the Sequence Type "Rebound".*

Once the parser table is updated correctly, please upload your newick file containing these sequences. The resulting tree will be shown below. If you would like, you can download the visualization as a PDF. 