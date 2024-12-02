import pygame, random
from pygame import Vector2 as Vector2

renderscale = Vector2(1, 1)
camera = Vector2(0, 0)

pygame.init()
W, H=688, 500
#W, H=1600, 900
#W, H=400, 800
screen = pygame.display.set_mode([W, H])
clock = pygame.time.Clock()

FPS = 60

font = pygame.font.SysFont("Arial" , 12 , bold = True)

running = True

class objectmanager:
    def __init__(self):
        self.objects = []

    def tick_objects(self):
        for x in range(len(self.objects)):
            self.objects[x].apply_physics_tick(dt)

    def project_points(self, points : list, axis : Vector2):
        min = float('inf')
        max = float('-inf')

        for x in points:
            projection = x.dot(axis)

            if projection > max: max = projection
            if projection < min: min = projection

        return([min, max])

    def point_to_line_distance(self, point1, point2, point3):
        line = point2 - point1
        line_to_point = point3 - point1
        projection = line_to_point.dot(line)
        d = projection / line.length_squared()
        if d <= 0:
            closest_point = point1
        elif d >= 1:
            closest_point = point2
        else:
            closest_point = point1 + line * d
        distance = closest_point.distance_to(point3)

        return [distance, closest_point]

class physics_object:
    def __init__(self, controlable, center_of_mass:Vector2, initialConnected=[]):
        self.position = center_of_mass
        self.velocity = 0

        self.connectedPoints = []
        self.connectedPoints.extend(initialConnected)

        self.controlable = controlable
        self.speed = 2

    def apply_physics_tick(self, time):
        pass



class world:
    class rock:
        def __init__(self, center, pointNum, size):
            self.points = []
            for x in range(pointNum):
                    self.points.append(Vector2(random.normalvariate()*size+center[0], 
                                                random.normalvariate()*size+center[1]))
    
    def __init__(self, rockCount, rockSize, renderPointSize):
        self.SideOffset = rockSize*2
        self.PointNums = [50, 100]
        self.ArenaSize = [Vector2(0, 0), Vector2(688, 500)] #Total Arena
        self.TZSize = [Vector2(0, 0), Vector2(388, 300)] #TraversalZone
        self.StartSize = [Vector2(0, 300), Vector2(200, 500)]
        
        self.rockPoints = []
        
        for x in range(rockCount):
            newRock = world.rock(Vector2(random.randint(int(self.TZSize[0][0] + self.SideOffset), int(self.TZSize[1][0] - self.SideOffset)), 
                                        random.randint(int(self.TZSize[0][1] + self.SideOffset), int(self.TZSize[1][1] - self.SideOffset))), 
                                random.randint(self.PointNums[0], self.PointNums[1]), rockSize)
            self.rockPoints.extend(newRock.points)
        wallDistance = self.ArenaSize[1][1] - self.TZSize[1][1] - self.SideOffset
        maxRocks = int(wallDistance / (rockSize * 4))
        for x in range(maxRocks):
            newRock = world.rock(Vector2(self.TZSize[1][0], int(self.TZSize[1][1]) + (x/(maxRocks - 1)) * wallDistance),
                                random.randint(self.PointNums[0], self.PointNums[1]), rockSize)
            self.rockPoints.extend(newRock.points)
        
        self.renderPointSize = renderPointSize

    def drawRect(self, camera, color, pos1, pos2):
        pygame.draw.rect(screen, color, pygame.Rect(pos1[0] + camera[0], pos1[1] + camera[1], pos2[0] - pos1[0], pos2[1] - pos1[1]))

    def renderworld(self, camera):
        self.drawRect(camera, (100, 100, 100), self.ArenaSize[0], self.ArenaSize[1])
        self.drawRect(camera, (100, 50, 50), self.TZSize[0], self.TZSize[1])
        self.drawRect(camera, (100, 150, 0), self.StartSize[0], self.StartSize[1])
        for x in range(len(self.rockPoints)):
            pygame.draw.circle(screen, (255, 0, 0), self.rockPoints[x]+camera, self.renderPointSize)

    def updateCamera(self, keys, event):
        speed = 10

        if keys[pygame.K_LSHIFT]:
            speed = 100

        direction = Vector2(0, 0)
        if keys[pygame.K_LEFT]:
            direction[0] += 1
        if keys[pygame.K_RIGHT]:
            direction[0] += -1
        if keys[pygame.K_UP]:
            direction[1] += 1
        if keys[pygame.K_DOWN]:
            direction[1] += -1
        
        return direction * speed
def fps_counter():
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps , 1, pygame.Color("RED"))
    screen.blit(fps_t,(0,0))

object_manager = objectmanager()


arena = world(3, 9, 2)

while running:
    dt = clock.tick(FPS)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN: clickdown = True
        else: clickdown = False
        if event.type == pygame.MOUSEBUTTONUP: 
            clickup = True
        else: clickup = False
    
    camera += arena.updateCamera(pygame.key.get_pressed(), pygame.event.get())

    screen.fill((200, 200, 200))
    arena.renderworld(camera)

    #object_manager.tick_objects()

    #object_manager.handle_collisions()

    fps_counter()
    pygame.display.update()

pygame.quit()