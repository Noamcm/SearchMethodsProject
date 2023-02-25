import time
import timeit
from statistics import mean

from aStar import a_star
from AL_star import a_star_lookahead
import TilePuzzle


def main():
    levels = ["easy", "medium", "hard", "extreme", "unsolvable"]  # "medium" 18.459 "hard" 26.7 "extreme" 52.86
    heuristics = ["manhattan", "euclidean", "empty"]
    puzzle_sizes = [8,15]
    algorithms = [a_star, a_star_lookahead]

    level = "medium"
    heuristic = "manhattan"
    puzzle_size = 8
    k = 5
    algorithm = a_star_lookahead

    tile_puzzle = TilePuzzle.TilePuzzle(puzzle_size, level, heuristic)

    times = []
    for i in range(10):
        print(i)
        start = time.time()
        # print(a_star_lookahead(tile_puzzle, k=k))
        print(algorithm(tile_puzzle))
        finish = time.time()
        times.append(finish - start)
    print(algorithm.__name__, str(puzzle_size)+" tile puzzle", "k="+str(k), level, heuristic,  round(mean(times), 3))


if __name__ == "__main__":
    main()
