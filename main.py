import logging
from collections import deque
from logging.config import fileConfig
from typing import TextIO

fileConfig("log.ini")

logger = logging.getLogger("dev")


def get_input_data(filename: str) -> tuple[deque[int], deque[int]]:
    f: TextIO = open(filename)

    player_1: deque[int] = deque()
    player_2: deque[int] = deque()

    f.readline()
    current_line = f.readline().strip()

    while current_line != "":
        player_1.append(int(current_line))
        current_line = f.readline().strip()

    f.readline()
    current_line = f.readline().strip()

    while current_line != "":
        player_2.append(int(current_line))
        current_line = f.readline().strip()

    f.close()

    return player_1, player_2


def play_one_round(player_1: deque[int], player_2: deque[int]):
    card_1 = player_1.popleft()
    card_2 = player_2.popleft()

    if card_1 < card_2:
        player_2.append(card_2)
        player_2.append(card_1)
    else:
        player_1.append(card_1)
        player_1.append(card_2)


def count_score(winning_player: deque[int]):
    winning_player.reverse()
    weight: int = 1
    score: int = 0
    for card in winning_player:
        score += card * weight
        weight += 1
    return score


def cycle_rec_game(player_1: deque[int], player_2: deque[int]):
    card_1 = player_1.popleft()
    card_2 = player_2.popleft()

    if card_1 <= len(player_1) and card_2 <= len(player_2):
        winner_sub = play_rec_game(deque(list(player_1)[:card_1]), deque(list(player_2)[:card_2]))
        if winner_sub == 1:
            player_1.append(card_1)
            player_1.append(card_2)
        else:
            player_2.append(card_2)
            player_2.append(card_1)
    else:
        if card_1 < card_2:
            player_2.append(card_2)
            player_2.append(card_1)
        else:
            player_1.append(card_1)
            player_1.append(card_2)


def play_rec_game(player_1: deque[int], player_2: deque[int]) -> int:
    memory_1: list[list[int]] = []
    memory_2: list[list[int]] = []

    while (len(player_1) > 0) and (len(player_2) > 0):

        if list(player_1) in memory_1 or list(player_2) in memory_2:
            return 1

        memory_1.append(list(player_1))
        memory_2.append(list(player_2))

        logger.debug(f"Player 1: {player_1}, Player 2: {player_2}")

        cycle_rec_game(player_1, player_2)

    if len(player_1) == 0:
        return 2
    else:
        return 1


def solution_part_1(filename: str) -> int:
    player_1, player_2 = get_input_data(filename)
    logger.debug(f"Player 1: {player_1}, Player 2: {player_2}")
    while (len(player_2) > 0) and (len(player_1) > 0):
        play_one_round(player_1, player_2)
        logger.debug(f"Player 1: {player_1}, Player 2: {player_2}")
    if len(player_1) == 0:
        return count_score(player_2)
    else:
        return count_score(player_1)


def solution_part_2(filename: str) -> int:
    player_1, player_2 = get_input_data(filename)
    winner = play_rec_game(player_1, player_2)
    logger.debug(winner)

    if winner == 1:
        return count_score(player_1)
    else:
        return count_score(player_2)


if __name__ == '__main__':
    logger.info(solution_part_1("inputData.txt"))
    logger.info(solution_part_2("inputData.txt"))
