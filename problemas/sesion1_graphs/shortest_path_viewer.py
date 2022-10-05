from algoritmia.viewers.labyrinth_viewer import LabyrinthViewer

from shortest_path import process

if __name__ == '__main__':
    g, path = process(2500, 2500)
    lv = LabyrinthViewer(g)
    lv.add_path(path)

    lv.run()