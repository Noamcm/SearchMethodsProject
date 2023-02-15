import timeit

import aStar
import idaStar
import heuristics


def main():
    easy_start_state = [[1, 2, 3], [5, 6, 0], [7, 8, 4]]
    difficult_start_state = [[8, 7, 6], [5, 4, 3], [2, 1, 0]]


    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    euclidean_heuristic = heuristics.euclidean_distance_heuristic
    manhattan_heuristic = heuristics.manhattan_distance_heuristic()
    empty_heuristic = heuristics.empty_heuristic()
   
   
   
    aStarEuc = aStar.a_star(difficult_start_state, goal_state,euclidean_heuristic)
    idaStarEuc = idaStar.ida_star(difficult_start_state, goal_state,euclidean_heuristic)
    print("euclidean A* result : "+ str(aStarEuc))
    print("euclidean IDA*  result: "+ str(idaStarEuc))
    
    aStarM = aStar.a_star(difficult_start_state, goal_state,manhattan_heuristic)
    idaStarM = idaStar.ida_star(difficult_start_state, goal_state,manhattan_heuristic)
    print("manhattan A* result : "+ str(aStarM))
    print("manhattan IDA*  result: "+ str(idaStarM))
    
    aStarEmp = aStar.a_star(difficult_start_state, goal_state,empty_heuristic)
    idaStarEmp = idaStar.ida_star(difficult_start_state, goal_state,empty_heuristic)
    print("empty A* result: "+ str(aStarEmp))
    print("empty  IDA* result: "+ str(idaStarEmp))

if __name__ == "__main__":
    main()
