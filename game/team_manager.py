import random
from agent.agent import Agent
from config import get_asset_path


class TeamManager:
    def __init__(self, game_map, player):
        self.team_a = []
        self.team_b = []
        self.all_agents = []

        # Dodaj gracza do team A
        player.team_id = 0
        self.team_a.append(player)

        # Spawn Team A
        for i in range(2):
            agent = Agent(get_asset_path("../images/DarkRanger.png"), 100 + i * 40, 100, game_map, team_id=0)
            self.team_a.append(agent)

        # Spawn Team B
        for i in range(2):
            agent = Agent(get_asset_path("../images/DarkRangerGreen.png"), 400 + i * 40, 400, game_map, team_id=1)
            self.team_b.append(agent)

        self.all_agents = self.team_a + self.team_b

    def update(self, dt):
        for agent in self.all_agents:
            agent.update(dt)

    def draw(self, surface, camera):
        for agent in self.all_agents:
            agent.draw(surface, camera)