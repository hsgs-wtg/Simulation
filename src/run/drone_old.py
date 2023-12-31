import math
import pygame

COLOR_BLUE = (0, 0, 255)
COLOR_FILLED = (204, 201, 72, 128)

# Create a drone
class Drone:
    def __init__(self, capacity, max_battery, spray_range, pump_speed, terminal_points):
        self.capacity = capacity
        self.max_battery = max_battery

        self.current_battery = max_battery
        self.current_weight = capacity

        self.spray_range = spray_range
        self.pump_speed = pump_speed
        
        self.terminal_points = terminal_points


        self.spray = []
        self.last_spray = []

        # Formula has signature f(current_weight, pump_speed)
        self.formula = None

    def get_battery_consumption(self):
        F_p = self.pump_speed if (self.current_weight > 0) else 0
        return self.formula(self.current_weight, F_p)
    
    def consume_pesticide(self, time):
        consumption = (self.pump_speed / 3600) * time
        self.current_weight = max(0, self.current_weight - consumption)

    def consume_battery(self, time):
        self.current_battery = max(0, self.current_battery - self.get_battery_consumption() * time)

    def set_draw(self, region, rw, rh):
        # type of region is ((x1, y1), (x2, y2))
        self.region = region
        self.rw = rw
        self.rh = rh

    def set_start_position(self, x, y):
        self.position = [x, y]
        self.update_spray()

    def set_movement(self, dx, dy):
        self.movement = [dx, dy]
        self.update_spray()

    def update_spray(self):
        try:
            mult = (self.spray_range / 2) / math.sqrt(self.movement[0] ** 2 + self.movement[1] ** 2)
            self.alt_movement = [self.movement[1], -self.movement[0]]
            self.last_spray = self.spray
            self.spray = [
                [self.position[0] - self.alt_movement[0] * mult, self.position[1] - self.alt_movement[1] * mult],
                [self.position[0] + self.alt_movement[0] * mult, self.position[1] + self.alt_movement[1] * mult]
            ]

            if not self.last_spray:
                self.last_spray = self.spray
            
            sign_x = 1 if (self.last_spray[0][0] < self.spray[0][0]) else -1
            sign_y = 1 if (self.last_spray[0][1] < self.spray[0][1]) else -1
            
            sign_x *= 0.5
            sign_y *= 0.5

            self.last_spray[0][0] -= sign_x
            self.last_spray[1][0] -= sign_x
            self.spray[0][0] += sign_x
            self.spray[1][0] += sign_x

            self.last_spray[0][1] -= sign_y
            self.last_spray[1][1] -= sign_y
            self.spray[0][1] += sign_y
            self.spray[1][1] += sign_y
        except ZeroDivisionError as e:
            pass

    def process(self):
        for d in range(2):
            self.position[d] += self.movement[d]
        self.update_spray()

    def convert(self, x, y):
        altx = round(self.region[0][0] + x * self.rw)
        alty = round(self.region[1][1] - y * self.rh)
        return altx, alty
    
    def pixel(self):
        return self.convert(*self.position)

    def draw_drone(self, surface):
        X, Y = self.convert(*self.position)

        pygame.draw.circle(surface,
                           color = COLOR_BLUE,
                           center = (X, Y),
                           radius = 3,
                           width = 0)

    def draw_spray(self, surface):
        points = [self.convert(*i) for i in self.last_spray + self.spray[::-1]]
        

        pygame.draw.polygon(surface,
                            color = COLOR_FILLED,
                            points = points,
                            width = 0)
