import sys
import turtle as tt
from find_way import dac_find_path
from find_way import dijkstra_find_path
from find_way import astar_find_path
import os
import GUI
import GUI_V2 as gv2
import time


def poly_moving(m_find_path, turtle):
    direct = 2
    while m_find_path.current_pos != m_find_path.goal:
        m_find_path.poly_move(direct)
        direct = (direct + 4) % 8
        matrix = m_find_path.map_mat
        print(matrix)
        # GUI.fillColorOneElementOnGridByMatrix(turtle, matrix, GUI.LENGTH)
        m_find_path.next_move()
        (x, y) = m_find_path.current_pos
        # GUI.fillDotOnGrid(turtle, x, y, GUI.LENGTH)


def main():
    if (len(sys.argv) == 4 and (sys.argv[2] in ['0', '1', '2', '3']) and (sys.argv[3] in ['turtle', 'pygame'])):
        input_filepath = sys.argv[1]

        if not (os.path.exists(input_filepath)):
            print("File does not exist! ")
            return

        find_algo = sys.argv[2]
        if find_algo == '0':
            m_find_path = dijkstra_find_path.Dijkstra_Find_Path(input_filepath)
            time_start = time.time()
            path = m_find_path.get_path()
            time_end = time.time()
            m_find_path.update_map_mat()
            matrix = m_find_path.map_mat
        if find_algo == '1':
            m_find_path = astar_find_path.AStar_Find_Path(input_filepath)
            time_start = time.time()
            path = m_find_path.get_path()
            time_end = time.time()
            m_find_path.update_map_mat()
            matrix = m_find_path.map_mat
        if find_algo == '2':
            m_find_path = dac_find_path.Dac_Find_Path(input_filepath)
            time_start = time.time()
            path = m_find_path.get_path()
            time_end = time.time()
            m_find_path.update_map_mat()
            matrix = m_find_path.map_mat

        if find_algo == "3":
            #m_find_path = dac_find_path.Dac_Find_Path(input_filepath)
            #m_find_path.update_map_mat()
            #path = (0, [])
            #matrix = m_find_path.map_mat

            screen = tt.Screen()
            Long = tt.Turtle()
            Long.hideturtle()
            turtle = Long
            tt.tracer(0, 0)

            m_find_path = astar_find_path.AStar_Find_Path(input_filepath)

            path = []
            while 1:
                matrix = m_find_path.get_matrix()
                check, tmp_path = m_find_path.move()
                path = path + tmp_path
                #print(check)

                GUI.grid(turtle, len(matrix), len(matrix[0]))
                GUI.fillColorOneElementOnGridByMatrix(turtle, matrix, GUI.LENGTH)
                GUI.findWay(turtle, path, matrix, GUI.LENGTH)
                #break
                if check == True:
                    break

            screen.exitonclick()


        #print(time_end - time_start)

        if find_algo == '3':
            return

        if sys.argv[3] == "turtle":
            path1 = path[1]
            screen = tt.Screen()
            Long = tt.Turtle()
            Long.hideturtle()
            turtle = Long
            tt.tracer(0, 0)

            GUI.grid(turtle, len(matrix), len(matrix[0]))
            GUI.fillColorOneElementOnGridByMatrix(turtle, matrix, GUI.LENGTH)
            GUI.findWay(turtle, path1, matrix, GUI.LENGTH)

            screen.exitonclick()

        if find_algo == '3':
            poly_moving(m_find_path, turtle)
        elif sys.argv[3] == "pygame":
            surface = gv2.init(matrix)
            gv2.loop(surface, matrix, path)
    else:
        print("Usage:", sys.argv[0], 'input_filepath', 'type_algo(0-2)', 'type_gui(turtle or pygame)')


if __name__ == '__main__':
    main()