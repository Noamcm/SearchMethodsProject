import time
import timeit
from statistics import mean

from aStar import a_star
from AL_star import a_star_lookahead
import TilePuzzle


def main():
    levels = ["easy", "medium", "hard"]
    heuristics = ["hamming", "euclidean", "manhattan"]

    for h in heuristics:
        for l in levels:
            level = l
            heuristic = h
            puzzle_size = 8
            k = 4
            algorithm = a_star
            algorithm_name = str(algorithm.__name__)
            tile_puzzle = TilePuzzle.TilePuzzle(puzzle_size, level, heuristic, algorithm_name)

            algorithm = a_star_lookahead
            times = []
            lengths = []
            expand=[]
            lookahead=[]
            dup=[]

            for i in range(1000):
                start = time.time()
                len_moves, moves, total_expand, total_found_lookahead, total_found_again = (algorithm(tile_puzzle, k=k, check_lookahead_closed=False))
                finish = time.time()
                times.append(finish - start)
                lengths.append(len_moves)
                expand.append(total_expand)
                lookahead.append(total_found_lookahead)
                dup.append(total_found_again)
            print(algorithm.__name__, str(puzzle_size)+" tile puzzle", "k="+str(k), level, heuristic,"avg time: ",round(mean(times), 10),"avg expanded nodes: ",  round(mean(expand), 10),"avg lookahead nodes: ",  round(mean(lookahead), 10),"avg duplicated nodes: ",  round(mean(dup), 10) , "min: ",min(lengths), "max: ", max(lengths), "pruning= False")

            times = []
            lengths = []
            expand=[]
            lookahead=[]
            dup=[]

            for i in range(1000):
                start = time.time()
                len_moves, moves, total_expand, total_found_lookahead, total_found_again = (algorithm(tile_puzzle, k=k, check_lookahead_closed=True))
                finish = time.time()
                times.append(finish - start)
                lengths.append(len_moves)
                expand.append(total_expand)
                lookahead.append(total_found_lookahead)
                dup.append(total_found_again)
            print(algorithm.__name__, str(puzzle_size)+" tile puzzle", "k="+str(k), level, heuristic,"avg time: ",round(mean(times), 10),"avg expanded nodes: ",  round(mean(expand), 10),"avg lookahead nodes: ",  round(mean(lookahead), 10),"avg duplicated nodes: ",  round(mean(dup), 10) , "min: ",min(lengths), "max: ", max(lengths), "pruning= True")


if __name__ == "__main__":
    main()
