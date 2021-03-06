import math
import json
import random

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%d,%d)" % (self.x, self.y)
    
    def add(self,p):
        return Vector(self.x+p.x,self.y+p.y)

    def subtract(self,p):
        return Vector(self.x-p.x,self.y-p.y)

    def scale(self,a):
        return Vector(a*self.x,a*self.y)

    def dot(self,p):
        return self.x*p.x+self.y*p.y

    def cross(self,p):
        return self.x*p.y - self.y*p.x

    def mod2(self):
        return self.x*self.x + self.y*self.y

    def mod(self):
        return math.sqrt(self.mod2())

    def normalised(self):
        return Vector(self.x,self.y).scale(1/self.mod())


class Planet:
    def __init__(self, p, v, nid, r=1):
        self.position = p
        self.velocity = v
        self.radius = r
        self.mass = r**2
        self.elasticity = 1
        self.nid=nid
        self.num_boundaries = 0

    def intersects(self,p):
        return self.position.subtract(p.position).mod2() < math.pow(self.radius + p.radius,2)

    def accelerate(self,force,clock_tick):
        self.velocity = self.velocity.add(force.scale(clock_tick/self.mass)) 
        #adds to velocity vector

    def attract(self,otherp,clock_tick):
        between = self.position.subtract(otherp.position)
        dist = between.mod()
        force = 150*(self.mass * otherp.mass / dist ** 2)
        self.accelerate(between.scale(-force),clock_tick)
        otherp.accelerate(between.scale(force),clock_tick)
        #Scale force to clock tick?
        
    def move(self,clock_tick=1):
        self.position = self.position.add(self.velocity.scale(clock_tick))

    def update_mass(self, k = 1):
        om = self.mass
        self.mass = self.radius**2
        self.velocity = self.velocity.scale(k*om/self.mass+1-k)

def get_rebound_vectors(p1, p2):
    n = p2.position.subtract(p1.position).normalised()
    u1 = p1.velocity.dot(n)
    u2 = p2.velocity.dot(n)
    v1 = ((p1.mass-p2.mass)*u1 + 2*p2.mass*u2) / (p1.mass+p2.mass)
    v2 = ((p2.mass-p1.mass)*u2 + 2*p1.mass*u1) / (p1.mass+p2.mass)
    return (p1.velocity.subtract(n.scale(u1-v1)), p2.velocity.subtract(n.scale(u2-v2)))

class Universe:
    def __init__(self, R, r, extras=False):
        if extras:
            p1 = Planet(Vector(30,150), Vector(2,5),1, 30)
            p2 = Planet(Vector(100,50), Vector(2,-5), 500, 30)
            p3 = Planet(Vector(300,50), Vector(0,10), 20, 30)
            self.planets = [p1,p2,p3]
        else:
            self.planets = []
        self.map_radius = R
        self.elasticity = 0.95

        self.clock_tick = r

    def get_json(self):
        data = []
        for i,p in enumerate(self.planets):
            data.append({'x': p.position.x, 'y': p.position.y, 'r': p.radius,'id':p.nid, 's':p.num_boundaries})
        return json.dumps(data)

    def shrink(self,planet_id):
        #Selection by list comprehensilson? lol
        selected_planet = [x for x in self.planets if x.nid==planet_id][0]
        if (selected_planet.radius - 10 < 20): return
        selected_planet.radius -= 10
        selected_planet.update_mass(0.6);

    def grow(self,planet_id):
        selected_planet = [x for x in self.planets if x.nid==planet_id][0]
        if (selected_planet.radius + 10 > 80): return
        selected_planet.radius += 10
        selected_planet.update_mass()

    player_slots = [-1]

    def add_planet(self, competition_mode=True):
        new_id = random.randint(0,100000)
        ids = [x.nid for x in self.planets]
        ##To make sure Ids are unique lol
        while new_id in ids:
            new_id = random.randint(0,100000)
        
        p = Vector(self.map_radius, self.map_radius)
        if competition_mode:
            if all(i >= 0 for i in self.player_slots):
                self.player_slots = [j for i in self.player_slots for j in [i,-1]]
            for i,v in enumerate(self.player_slots):
                if v < 0:
                    self.player_slots[i] = new_id
                    t = math.pi*(-0.75 - 2*i/len(self.player_slots))
                    p = p.add(Vector(math.cos(t), math.sin(t)).scale(self.map_radius*0.6))
                    break

        ivel = 50
        newp = Planet(p,Vector(2*ivel*(random.random()-0.5),2*ivel*(random.random()-0.5)),new_id,20)
        self.planets.append(newp)
        return new_id

    def remove_planet(self,planet_id):
        ids = [x.nid for x in self.planets]
        self.player_slots = [-1 if i == planet_id else i for i in self.player_slots]
        if all(i < 0 for i in self.player_slots): self.player_slots = [-1]
        if planet_id in ids:
            remove_index = ids.index(planet_id)
            del self.planets[remove_index]
        

    def run_loop(self):

        for i in range(len(self.planets)):
            pos = self.planets[i].position
            rad = self.planets[i].radius

            # circular boundary
            cv = pos.subtract(Vector(self.map_radius, self.map_radius))
            if cv.mod() + rad > self.map_radius:
                self.planets[i].num_boundaries += 1
                n = cv.normalised()
                v = self.planets[i].velocity
                u = n.scale(v.dot(n))
                self.planets[i].velocity = v.subtract(n.scale((1+self.elasticity)*v.dot(n)))
                self.planets[i].position = pos.subtract(n.scale(cv.mod() + rad - self.map_radius))

            # bouncing
            for j in range(i):
                p1 = self.planets[i]
                p2 = self.planets[j]
                if p1.intersects(p2):
                    vi, vj = get_rebound_vectors(p1,p2)
                    p1.velocity = vi
                    p2.velocity = vj

                    ##Fix for intersecting
                    o = p1.radius + p2.radius - p1.position.subtract(p2.position).mod()
                    n = p2.position.subtract(p1.position).normalised()
                    p2.position = p2.position.add(n.scale(o/2))
                    p1.position = p1.position.add(n.scale(-o/2))

                p1.attract(p2,self.clock_tick)

        for p in self.planets:
            p.move(self.clock_tick)
            
            #self.planets[i].position = pos.add(self.planets[i].velocity.scale(self.clock_tick))
            






