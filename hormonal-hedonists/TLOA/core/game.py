from TLOA.core.constants import Actions, SHIP_SCORE, LANE_NUMBER
from TLOA.entities import MirrorCannon
from TLOA.entities import GoldenShip, BrownShip, ShipType

from kivy import Logger
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import ListProperty, NumericProperty, BoundedNumericProperty
from random import randint


class Game(EventDispatcher):
    score = NumericProperty(0)
    health = BoundedNumericProperty(100, min=0, max=100,
                                    errorhandler=lambda x: 0 if x < 0 else 100)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mirror = MirrorCannon()
        self.ships = []
        self.total_spawned_ship = 0
        self.view = None

    def start(self, view):
        Logger.info('Start game')
        self.view = view
        Clock.schedule_interval(self.spawn_ship, 5)


    def process_action(self, action: Actions):
        if action == Actions.MOVE_LEFT:
            print('Moving Left')
            self.mirror.state -= 1
        elif action == Actions.MOVE_RIGHT:
            print('Moving Right')
            self.mirror.state += 1
        elif action == Actions.MOVE_UP:
            print('Moving Up')
        elif action == Actions.MOVE_DOWN:
            print('Moving Down')
        return True


    def spawn_ship(self, dt):
        self.total_spawned_ship += 1
        # TODO instead of create new ship, we can use existing one, so no need allocate new memory
        if self.total_spawned_ship % 10 == 0:
            # after 9 brown ships, we add new 1 golden ship
            Logger.info('Spawn new golden ship')
            new_ship = GoldenShip()
        else:
            Logger.info('Spawn new brown ship')
            new_ship = BrownShip()
        ship_lane = randint(0, LANE_NUMBER - 1)
        new_ship.bind(destroyed=self.on_ship_destroyed)
        self.ships.append((new_ship, ship_lane))
        self.view.show_ship(new_ship, ship_lane)

    def on_ship_destroyed(self, ship, new_state):
        if new_state:
            self.score += SHIP_SCORE[ship._type]
            # ship is destroyed, remove it from view
            Logger.info('Remove ship')
            for ship_info in self.ships:
                if ship_info[0] == ship:
                    self.ships.remove(ship_info)

    def on_health(self, obj, value):
        Logger.info(f'Island health: {value}')
        if value <= 0:
            Logger.info('Game Over')
    
    def on_ship_attack(self, animation, ship):
        Logger.info('Ship attacked')
        # reduce health
        # TODO add more logic to calculate reduced health, like base on ship type, ship health
        self.health -= 10