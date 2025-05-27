"""
tree-render-functions.py
    This python file accepts a tree file and a 
    dataframe as a csv and generates a tree
    visualization by collapsing clones.
    Its saves the files as a PNG/PDF that is
    used by the main app. 
    For more information see:
    https://github.com/walkerazam/cohn-treemaker
"""
import pandas as pd
import numpy as np
import sys
from io import StringIO
import os
os.environ['QT_QPA_PLATFORM']='offscreen'
import re

from ete3 import Tree, TreeStyle, PhyloTree, TextFace, NodeStyle, SeqMotifFace
from ete3 import faces, AttrFace, CircleFace, TextFace, RectFace

def render_tree(treefile, df_csv, kwargs, class_csv=None):
    # Reading in newick tree file 
    t = Tree(treefile) # Tree not PhyloTree!
    # Deserialize the parser df DataFrame
    parser_df = pd.read_csv(StringIO(df_csv))

    # Deserialize kwargs and set values
    kwargs = pd.read_csv(StringIO(kwargs))
    ts_scale = kwargs["ts_scale"].iloc[0]
    clone_threshold = kwargs["clone_threshold"].iloc[0]
    leaf_name_bool = kwargs["leaf_name_bool"].iloc[0]
    rooting_node = kwargs["rooting_node"].iloc[0]

    if class_csv is not None:
        class_df = pd.read_csv(StringIO(class_csv))
        classification_default = class_df.loc[1, "Classification"] # circle
        classification_alternate = class_df.loc[0, "Classification"] # square
        class_parser = class_df.loc[0, "Parser"] # parser for squares
    else:
        classification_default = "default"
        classification_alternate = "alternate"

    # Midpoint rooting tree
    if rooting_node == 'midpoint':
        midpoint = t.get_midpoint_outgroup()
    elif t.search_nodes(name=rooting_node):  # if the node is not valid, then reverts to midpoint
        midpoint = rooting_node
    else:
        midpoint = t.get_midpoint_outgroup()
    t.set_outgroup(midpoint)
    # Ladderize tree
    t.ladderize()

    # annotating Sequence Type
    for leaf in t.iter_leaves():
        leaf_name = leaf.name # get leaf name
        if class_csv is not None:
            leaf.add_feature("Classification", classification_default)
            if re.search(class_parser, leaf_name):
                leaf.add_feature("Classification", classification_alternate)
            else:
                leaf.add_feature("Classification", classification_default)
        else:
            leaf.add_feature("Classification", classification_default)
        found_match = False # check for is a parser was matched
        for index, row in parser_df.iterrows():
            # check for parser in leaf name
            if re.search(str(row["Parser"]), leaf_name):
                leaf.add_feature("SeqType", row["SeqType"]) # add as a feature of the leaf
                found_match = True # flip to true
                break  # if a match found, exit loop and move to next leaf
        if not found_match:
            leaf.add_feature("SeqType", False)

    # # verify your SeqTypes are being annotated correctly:
    # for leaf in t.iter_leaves():
    #     print(leaf.name, leaf.SeqType)

    # Dataframe to track different SeqTypes that are clones
    df_cols = parser_df['SeqType'].to_list()

    unmapped = False # toggle for unmapped seqs
    for leaf in t.iter_leaves():
        if leaf.SeqType is False:
            unmapped = True # flip on if False found
    # if unmapped seqs exist, then add that to df_cols
    if unmapped:
        df_cols.append(False)

    leaf_df = pd.DataFrame(index = [leaf.name for leaf in t.iter_leaves()], columns = df_cols)
    leaf_df = leaf_df.fillna(0)

    # Add Definition for Weight:
    # Weigth if the # of clones, and which nodes should be removed in place
    threshold = clone_threshold # default value = 1e-06 # set threshold to be ~1 mutation (double check)

    def leaf_distance(leaf1, leaf2):
        """
        This function returns the distance between two leaves
        """
        return t.get_distance(leaf1, leaf2)

    # Iterate through each leaf
    checked_neighbors = set() # set of every node that has been 'accounted' for
    # create a dictionary of dictionaries to track shapes per node:
    node_shape_list = {}

    # for every leaf...
    for leaf in t.iter_leaves():
        # create a dict for the node:
        shapes_dict = {}
        if leaf in checked_neighbors:
            # make sure it wasn't already counted for...
            leaf.add_feature("Weight", -1)
        else:
            weight = 0  # set counter to 0 
            # check every other leaf
            for other_leaf in t.iter_leaves():
                # Exclude the same leaf AND check its not already accounted for
                if other_leaf != leaf and other_leaf not in checked_neighbors:
                    distance = leaf_distance(leaf, other_leaf) # get distance
                    # if distance passes AND same SeqType
                    if distance <= threshold and leaf.SeqType == other_leaf.SeqType: 
                        # add to counter and mark as counted for 
                        weight += 1
                        checked_neighbors.add(other_leaf)
                    elif distance <= threshold and leaf.SeqType != other_leaf.SeqType:
                        leaf_df.loc[leaf.name, other_leaf.SeqType] = leaf_df.loc[leaf.name, other_leaf.SeqType] + 1
                        checked_neighbors.add(other_leaf)
                        if other_leaf.Classification != leaf.Classification:
                            if other_leaf.SeqType in shapes_dict.keys():
                                shapes_dict[other_leaf.SeqType] = shapes_dict[other_leaf.SeqType] + 1 
                            else:
                                shapes_dict[other_leaf.SeqType] = 1
            # Assign the weight as a feature to the leaf
            leaf.add_feature("Weight", weight)
            # mark the current leaf as also counted for 
            checked_neighbors.add(leaf)
            # add shapes_dict to list
            node_shape_list[leaf.name] = shapes_dict

    leaves_to_keep = [] # empty list of leaves to keep
    # keep leaves that have a weight 
    for leaf in t.iter_leaves():
        if leaf.Weight != -1:
            leaves_to_keep.append(leaf)
    # remove nodes that are clonal from shape list
    for x in leaves_to_keep:
        if x in node_shape_list:
            node_shape_list.pop(x.name)
    # drop leaves with weight = -1 while preserving branch lengths
    t.prune(leaves_to_keep, preserve_branch_length=True)

    # Colormap for seq type
    seqtype_cmap = dict(zip(parser_df['SeqType'], parser_df['Color']))
    # add default black for False seqtype (unmapped)
    if unmapped:
        seqtype_cmap[False] = 'black'

    # Setting node style
    def set_seqtype_color(node):
        if "SeqType" in node.features:
            if node.Classification == classification_default:
                nstyle = NodeStyle()
                nstyle["fgcolor"] = seqtype_cmap[node.SeqType]
                nstyle["size"] = 8
                nstyle["hz_line_width"] = 2
                node.set_style(nstyle) 
            elif node.Classification == classification_alternate:
                nstyle = NodeStyle()
                nstyle["shape"] = "square"
                nstyle["fgcolor"] = seqtype_cmap[node.SeqType]
                nstyle["size"] = 6
                nstyle["hz_line_width"] = 2
                node.set_style(nstyle) 
    def make_branches_bigger(node, new_size):
        node.img_style["size"] = 0
        node.img_style["hz_line_width"] = new_size # Change the horizotal lines stroke size
        node.img_style["vt_line_width"] = new_size # Change the vertical lines stroke size
    for node in t.traverse():
        set_seqtype_color(node)
        for c in node.children:
            make_branches_bigger(c, 2)

    # plotting entire tree
    ts = TreeStyle()
    #ts.show_leaf_name = False
    
    def custom_layout(node):
        """
        This function creates the stacking of clonal sequences
        """
        if 'Classification' in node.features:
            if node.Classification != classification_alternate:
                if node.Weight != -1:
                    for i in range(node.Weight):
                        faces.add_face_to_node(faces.CircleFace(4, seqtype_cmap[node.SeqType]), 
                                        node, column=i*2+1, position="branch-right")
                    spot_sum = node.Weight
                    # Go through the DF of different SeqTypes
                    if leaf_df.loc[node.name].sum() > 0:
                        for seq_type_i in df_cols:
                            # if alternate shape present in node_shape_list track how many of that seq type
                            shape_dict = node_shape_list[node.name]
                            if seq_type_i in shape_dict.keys():
                                alt_value = shape_dict[seq_type_i]
                            else:
                                alt_value = 0 
                                
                            range_val = leaf_df.loc[node.name, seq_type_i]
                            new_range_val = range_val - alt_value
                            for i in range(new_range_val):
                                faces.add_face_to_node(faces.CircleFace(4, seqtype_cmap[seq_type_i]), 
                                                    node, column=spot_sum*2+1, position="branch-right")
                                spot_sum += 1
                            for i in range(alt_value):
                                faces.add_face_to_node(faces.RectFace(8, 8, 'white',seqtype_cmap[seq_type_i]), 
                                                node, column=spot_sum*2+1.02, position="branch-right")
                                spot_sum += 1
            # for classification_alternate
            else:
                if node.Weight != -1:
                    for i in range(node.Weight):
                        faces.add_face_to_node(faces.RectFace(8, 8, 'white', seqtype_cmap[node.SeqType]), 
                                    node, column=i*2, position="branch-right")
                    spot_sum = node.Weight
                    # Go through the DF of different SeqTypes
                    if leaf_df.loc[node.name].sum() > 0:
                        for seq_type_i in df_cols:
                            # if default shape present in node_shape_list track how many of that seq type
                            shape_dict = node_shape_list[node.name]
                            if seq_type_i in shape_dict.keys():
                                alt_value = shape_dict[seq_type_i]
                            else:
                                alt_value = 0
                                
                            range_val = leaf_df.loc[node.name, seq_type_i]
                            new_range_val = range_val - alt_value
                            for i in range(new_range_val):
                                faces.add_face_to_node(faces.RectFace(8, 8, 'white',seqtype_cmap[seq_type_i]), 
                                                node, column=spot_sum*2+1.02, position="branch-right")
                                spot_sum += 1
                            for i in range(alt_value):
                                faces.add_face_to_node(faces.CircleFace(4, seqtype_cmap[seq_type_i]), 
                                                    node, column=spot_sum*2+1, position="branch-right")
                                spot_sum += 1
    
    ts.layout_fn = custom_layout

    ts.margin_left = 20
    ts.margin_right = 20
    ts.margin_top = 20

    # Setting root node
    rootstyle = NodeStyle()
    rootstyle["size"] = 3
    rootstyle["fgcolor"] = 'black'
    rootstyle["shape"] = "square"
    rootstyle["vt_line_width"] = 2
    rootstyle["hz_line_width"] = 2
    t.set_style(rootstyle)

    # LEGEND INFORMATION
    for key, val in seqtype_cmap.items():
        if key:  # for unmapped sequences, don't populate legend
            ts.legend.add_face(TextFace(f" {key} ", fsize=12, ftype='Arial'), column=1)
            ts.legend.add_face(CircleFace(3, val), column=0)
        else:
            ts.legend.add_face(TextFace(f" Undefined Sequence ", fsize=12, ftype='Arial'), column=1)
            ts.legend.add_face(CircleFace(3, val), column=0)
    ts.legend_position = 2

    if class_csv is not None:
        ts.legend.add_face(TextFace(f" {classification_alternate}", fsize=12, ftype='Arial'), column=3)
        ts.legend.add_face(RectFace(8,8,"black", "white"), column=2)
        ts.legend.add_face(TextFace(f" {classification_default}", fsize=12, ftype='Arial'), column=3)
        ts.legend.add_face(CircleFace(3,"black"), column=2)

    # more space between branches
    ts.branch_vertical_margin = 2
    ts.scale = ts_scale # def = 10000
    ts.show_leaf_name = leaf_name_bool # def = False

    # saving the plots as both a png for visualizing and a pdf for downloading
    t.render("data/tree-file.pdf", tree_style=ts, w=4, dpi=200, units='in')
    t.render("data/tree-file.png", tree_style=ts, w=4, dpi=200, units='in')


if __name__ == "__main__":
    # Get the file path from the subprocess command-line arguments
    if len(sys.argv) > 4:
        treefile = sys.argv[1]
        df_csv = sys.argv[2]
        class_csv = sys.argv[3]
        kwargs = sys.argv[4]
        render_tree(treefile, df_csv, kwargs, class_csv)
    elif len(sys.argv) > 3:
        treefile = sys.argv[1]
        df_csv = sys.argv[2]
        kwargs = sys.argv[3]
        render_tree(treefile, df_csv, kwargs, None)
    else:
        print("Error: No file provided.")