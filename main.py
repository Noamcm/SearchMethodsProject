import aStar
import idaStar
import euclideanDistanceHeuristic


def main():
    start_state = [[1, 2, 3], [5, 6, 0], [7, 8, 4]]
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    heuristic = euclideanDistanceHeuristic.heuristic

    solution1 = aStar.a_star(start_state, goal_state,heuristic)
    solution2 = idaStar.ida_star(start_state, goal_state,heuristic)

    print("A* result: "+ str(solution1))
    print("IDA*  result: "+ str(solution2))

if __name__ == "__main__":
    main()