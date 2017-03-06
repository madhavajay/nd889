from sample_players import HumanPlayer
from tournament import *
from game_agent import *


def main():
    AB_ARGS = {"search_depth": 5, "method": 'alphabeta', "iterative": False}
    agent_1 = Agent(HumanPlayer(), "Human")
    #agent_1 = Agent(CustomPlayer(score_fn=custom_score, **AB_ARGS), "Human")
    agent_2 = Agent(CustomPlayer(score_fn=improved_score, **AB_ARGS), "AB_Custom")
    agent_1_wins = 0.
    agent_2_wins = 0.
    total = 0.
    num_matches = 1

    print("\nPlaying Matches:")
    print("----------")

    counts = {agent_1.player: 0., agent_2.player: 0.}
    names = [agent_1.name, agent_2.name]
    print("  Match {}: {!s:^11} vs {!s:^11}".format(1, *names), end=' ')

    # Each player takes a turn going first
    for _ in range(num_matches):
        score_1, score_2 = play_match(agent_1.player, agent_2.player, True, 100000000)
        counts[agent_1.player] += score_1
        counts[agent_2.player] += score_2
        total += score_1 + score_2

    agent_1_wins += counts[agent_1.player]
    agent_2_wins += counts[agent_2.player]

    print("\tResult: {} to {}".format(int(counts[agent_1.player]),
                                      int(counts[agent_2.player])))

    agent_1_score = 100. * agent_1_wins / total
    print('Score: {}'.format(agent_1_score))


if __name__ == "__main__":
    main()
