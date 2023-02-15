import aStar
import idaStar
import euclideanDistanceHeuristic
import emptyHeuristic


def main():
    easy_start_state = [[1, 2, 3], [5, 6, 0], [7, 8, 4]]
    difficult_start_state = [[8, 7, 6], [5, 4, 3], [2, 1, 0]]


    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    heuristic = euclideanDistanceHeuristic.heuristic
    heuristice = emptyHeuristic.heuristic

    solution1 = aStar.a_star(difficult_start_state, goal_state,heuristic)
    solution2 = idaStar.ida_star(difficult_start_state, goal_state,heuristic)
    print("A* result : "+ str(solution1))
    print("IDA*  result: "+ str(solution2))

    solution1e = aStar.a_star(difficult_start_state, goal_state,heuristice)
    solution2e = idaStar.ida_star(difficult_start_state, goal_state,heuristice)

    print("A* empty result: "+ str(solution1e))
    print("IDA* empty  result: "+ str(solution2e))

if __name__ == "__main__":
    main()