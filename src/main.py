import sys
#import turtle as tt
from find_way import dac_find_path
from find_way import dijkstra_find_path
from find_way import astar_find_path
import os
#import GUI
import GUI_V2 as gv2

def main():
    if (len(sys.argv) == 3 and (sys.argv[2] == '0' or sys.argv[2] == '1' or sys.argv[2] == '2')):
        input_filepath = sys.argv[1]

        if not (os.path.exists(input_filepath)):
            print("File does not exist! ")
            return

        find_algo = sys.argv[2]
        if find_algo == '0':
            m_find_path = dijkstra_find_path.Dijkstra_Find_Path(input_filepath)
            path = m_find_path.get_path()
            m_find_path.update_map_mat()
            matrix = m_find_path.map_mat
        if find_algo == '1':
            m_find_path = astar_find_path.AStar_Find_Path(input_filepath)
            path = m_find_path.get_path()
            m_find_path.update_map_mat()
            matrix = m_find_path.map_mat
        if find_algo == '2':
            m_find_path = dac_find_path.Dac_Find_Path(input_filepath)
            path = m_find_path.get_path()
            m_find_path.update_map_mat()
            matrix = m_find_path.map_mat

        # #test
        # path1 = path[1]

        # Long = tt.Turtle()
        # Long.hideturtle()
        # turtle = Long

        # GUI.grid(turtle, len(matrix), len(matrix[0]))
        # GUI.fillColorOneElementOnGridByMatrix(turtle, matrix, GUI.LENGTH)
        # GUI.findWay(turtle, path1, GUI.LENGTH)

        # screen.exitonclick()
        surface = gv2.init(matrix)
        gv2.loop(surface, matrix, path)
    else:
        print("Usage:", sys.argv[0], 'input_filepath', 'type_algo_(0-2)')


if __name__ == '__main__':
    main()
