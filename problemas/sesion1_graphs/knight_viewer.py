from algoritmia.viewers.graph2d_viewer import Graph2dViewer

from knight_graph import process

if __name__ == '__main__':
    g, num_v_alcanzables = process(2, 10, 0, 0)
    print(f"Vertices alcanzables: {num_v_alcanzables}")
    gv = Graph2dViewer(g, vertexmode=Graph2dViewer.ROW_COL)

    gv.run()