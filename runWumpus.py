from Wumpus.Agent import Agent
from Wumpus.World import World
from time import sleep

if __name__ == "__main__":
    world = World()
    world.generate_world("world.txt")
    agent = Agent(world)

    agent.explore()
    if agent.found_gold:
        agent.leave_cave()
        print(agent)
        agent.world_knowledge[agent.world.agent_row][agent.world.agent_col].remove('A')
        sleep(2)
        print(agent)

    if agent.took_gold:
        print("wow, you have toke the gold!")
    else:
        print("It's pity that you miss the gold")

    print("Score:", agent.cal_score())
