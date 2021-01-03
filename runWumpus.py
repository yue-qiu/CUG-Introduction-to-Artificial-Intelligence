from Wumpus.Agent import Agent
from Wumpus.World import World

if __name__ == "__main__":
    world = World()
    world.generate_world("world.txt")
    agent = Agent(world)

    agent.explore()
    if agent.found_gold:
        print("wow, you have toke the gold!")
    else:
        print("It's pity that you miss the gold")

    print("Score:", agent.cal_score())
