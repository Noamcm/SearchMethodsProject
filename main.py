import time
import timeit
from statistics import mean

from aStar import a_star
from AL_star import a_star_lookahead
import TilePuzzle


def main():
    levels = ["easy", "medium", "hard", "extreme", "unsolvable"]  # "medium" 18.459 "hard" 26.7 "extreme" 52.86
    heuristics = ["manhattan", "hamming", "euclidean", "empty"]
    puzzle_sizes = [8,15]
    algorithms = [a_star, a_star_lookahead]

    level = "hard"
    heuristic = 'euclidean' #"manhattan"
    puzzle_size = 8
    k = 4
    algorithm = a_star_lookahead #a_star  / a_star_lookahead
    # algorithm_name = "a_star"
    algorithm_name = str(algorithm.__name__)

    tile_puzzle = TilePuzzle.TilePuzzle(puzzle_size, level, heuristic, algorithm_name)

    times = []
    lengths = []

    for i in range(1):
        #print(i)
        start = time.time()
        # len_moves, moves = a_star(tile_puzzle)
        len_moves, moves = (algorithm(tile_puzzle, k=k))
        #if i==0:
        print(len_moves, moves)
        lengths.append(len_moves)
        finish = time.time()
        times.append(finish - start)
    print(algorithm.__name__, str(puzzle_size)+" tile puzzle", "k="+str(k), level, heuristic,  round(mean(times), 3) , "min: ",min(lengths), "max: ", max(lengths))


if __name__ == "__main__":
    main()
