import re, heapq, math
from collections import defaultdict

ORE = 'ORE'
CLAY = 'CLAY'
OBSIDIAN = 'OBS'
GEODE = 'GEODE'

MAT_LIST = [GEODE, OBSIDIAN, CLAY, ORE]

class GeodeFactory:

    TIME_LIMIT = 0

    production_rate = {
        ORE: 1,
        CLAY: 0,
        OBSIDIAN: 0,
        GEODE: 0
    }

    inventory = {
        ORE: 0,
        CLAY: 0,
        OBSIDIAN: 0,
        GEODE: 0
    }

    def __init__(self, blueprint) -> None:
        self.clock = 0
        self.blueprint = blueprint

    def extract(self, minutes):
        for mat in MAT_LIST:
            self.inventory[mat] += self.production_rate[mat] * minutes
        self.clock += minutes

    def build(self, robot):
        for mat, cost in self.blueprint[robot].items():
            self.inventory[mat] -= cost
        self.production_rate[robot] += 1

    def clone(self):
        new_factory = GeodeFactory(self.blueprint)
        new_factory.clock = self.clock
        new_factory.production_rate = self.production_rate.copy()
        new_factory.inventory = self.inventory.copy()
        return new_factory

    @property
    def can_build(self):
        for robot in MAT_LIST:
            if all(self.production_rate[mat] > 0 for mat, _ in self.blueprint[robot].items()):
                if all(self.inventory[mat] - cost > 0 for mat, cost in self.blueprint[robot].items()):
                    yield robot, 1
                else:
                    yield robot, 1 + max(0, *[math.ceil(max(0, cost - self.inventory[mat]) / self.production_rate[mat]) for  mat, cost in self.blueprint[robot].items()])
    
    @property
    def prod_l(self):
        return tuple(self.production_rate[mat] for mat in MAT_LIST)

    @property
    def as_state(self):
        inv = ''.join(str(k)+str(v) for k, v in self.inventory.items())
        prod = ''.join(str(k)+str(v) for k, v in self.production_rate.items())
        return f'{self.clock},{inv},{prod}'

    @property
    def geode_extracted(self):
        return self.inventory[GEODE] + (self.TIME_LIMIT - self.clock) * self.production_rate[GEODE]

    def __lt__(self, o):
        return self.prod_l > o.prod_l
    
    def __repr__(self) -> str:
        return f'Factory: t{self.clock}\nInv: {self.inventory}\nRate: {self.production_rate}\nBuild: {list(self.can_build)}\n'

def main(day_input):
    full_input = '\n'.join(day_input)
    blueprints = re.findall(r'Blueprint (\d+):(?:\n )? Each ore robot costs (\d+) ore\.(?:\n )? Each clay robot costs (\d+) ore\.(?:\n )? Each obsidian robot costs (\d+) ore and (\d+) clay\.(?:\n )? Each geode robot costs (\d+) ore and (\d+) obsidian\.', full_input)

    def get_max_geode(start_factory):
        max_res = defaultdict(int)
        for _, res in start_factory.blueprint.items():
            for mat, cost in res.items():
                max_res[mat] = max(max_res[mat], cost)

        visited = set([])
        q = [start_factory]
        heapq.heapify(q)
        max_geode = 0

        while q:

            factory = heapq.heappop(q)
            geode = factory.geode_extracted
            if geode > max_geode:
                max_geode = geode

            for robot, time_to_build in factory.can_build:
                if factory.clock + time_to_build > factory.TIME_LIMIT: continue

                nf = factory.clone()
                nf.extract(time_to_build)
                nf.build(robot)

                # TY REDDIT FOR OPTIMIZATION! #
                timeleft = factory.TIME_LIMIT - nf.clock
                geodes_new_ideal = (timeleft-1)*(timeleft)//2
                geodes_final_ideal = nf.inventory[GEODE] + timeleft*nf.production_rate[GEODE] + geodes_new_ideal
                if geodes_final_ideal <= max_geode: continue
                ###############################

                if any(p > max_res[r] for r, p in nf.production_rate.items() if r != GEODE): continue
                if nf.as_state in visited: continue
                visited.add(nf.as_state)
                
                heapq.heappush(q, nf)
        

        return max_geode

    def map_factory(blueprint):
        (id,
        ore_robot_ore,
        clay_robot_ore,
        obsidian_robot_ore,
        obsidian_robot_clay,
        geode_robot_ore,
        geode_robot_obsidian) = map(int, blueprint)
        return id, GeodeFactory({
            ORE: { ORE: ore_robot_ore },
            CLAY: { ORE: clay_robot_ore },
            OBSIDIAN: { ORE: obsidian_robot_ore, CLAY: obsidian_robot_clay },
            GEODE: { ORE: geode_robot_ore, OBSIDIAN: geode_robot_obsidian }
        })

    GeodeFactory.TIME_LIMIT = 24
    quality_sum = 0
    factories = [map_factory(b) for b in blueprints]
    for id, factory in factories:
        quality = id * get_max_geode(factory)
        quality_sum += quality

    GeodeFactory.TIME_LIMIT = 32
    geo_prod = 1
    for id, factory in factories[:3]:
        geo_prod *= get_max_geode(factory)

    return quality_sum, geo_prod

