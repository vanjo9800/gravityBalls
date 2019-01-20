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

    def intersects(self,p):
        return self.position.subtract(p.position).mod2() < math.pow(self.radius + p.radius,2)

    def accelerate(self,otherp,clock_tick):
        self.velocity = self.velocity.add(otherp.scale(clock_tick)) 
        #adds to velocity vector

    def attract(self,otherp,clock_tick):
        between = self.position.subtract(otherp.position)
        dist = between.mod()
        force = 0.01*((self.mass * otherp.mass / dist ** 2)**1)
        self.accelerate(between.scale(-force),clock_tick)
        otherp.accelerate(between.scale(force),clock_tick)
        #Scale force to clock tick?
        
    def move(self,clock_tick=1):
        self.position = self.position.add(self.velocity.scale(clock_tick))

    def update_mass(self):
        om = self.mass
        self.mass = self.radius**2
        self.velocity = self.velocity.scale(om/self.mass)

def get_rebound_vectors(p1, p2):
    n = p2.position.subtract(p1.position).normalised()
    u1 = p1.velocity.dot(n)
    u2 = p2.velocity.dot(n)
    v1 = ((p1.mass-p2.mass)*u1 + 2*p2.mass*u2) / (p1.mass+p2.mass)
    v2 = ((p2.mass-p1.mass)*u2 + 2*p1.mass*u1) / (p1.mass+p2.mass)
    return (p1.velocity.subtract(n.scale(u1-v1)), p2.velocity.subtract(n.scale(u2-v2)))

class Universe:
    def __init__(self, w, h, r):
        p1 = Planet(Vector(30,150), Vector(20,100),0, 30)
        p2 = Planet(Vector(100,50), Vector(2,200), 1, 30)
        p3 = Planet(Vector(300,50), Vector(2,200), 2, 30)
        self.planets = [p1,p2,p3]
        self.width = w
        self.height = h
        self.elasticity = 0.9

        self.clock_tick = r

    def get_json(self):
        data = []
        for i,p in enumerate(self.planets):
            data.append({'x': p.position.x, 'y': p.position.y, 'r': p.radius,'id':p.nid})
        return json.dumps(data)

    def shrink(self,planet_id):
        #Selection by list comprehensilson? lol
        selected_planet = [x for x in self.planets if x.nid==planet_id][0]
        if (selected_planet.radius - 5 < 20): return
        selected_planet.radius -= 5
        selected_planet.update_mass()

    def grow(self,planet_id):
        selected_planet = [x for x in self.planets if x.nid==planet_id][0]
        if (selected_planet.radius + 5 > 100): return
        selected_planet.radius += 5
        selected_planet.update_mass()

    def add_planet(self):
        new_id = random.randint(1,1000)
        ids = [x.nid for x in self.planets]
        ##To make sure Ids are unique lol
        while new_id in ids:
            new_id = random.randint(1,1000)
        
        newp = Planet(Vector(self.width/2,self.height/2),Vector(0,0),new_id,20)
        self.planets.append(newp)
        return new_id

    def remove_planet(self,planet_id):
        ids = [x.nid for x in self.planets]
        remove_index = ids.index(planet_id)
        #Dangerous - del is overloaded
        del self.planets[remove_index]
        

    def run_loop(self):

        for i in range(len(self.planets)):
            pos = self.planets[i].position
            rad = self.planets[i].radius

            ##Boundary Checkr
            if pos.x - rad< 0: 
                self.planets[i].velocity.x *= -self.elasticity
                pos.x = 2*rad - pos.x
            if pos.x + rad> self.width: 
                self.planets[i].velocity.x *= -self.elasticity
                pos.x = 2*(self.width-rad) - pos.x
            if pos.y - rad< 0: 
                self.planets[i].velocity.y *= -self.elasticity
                pos.y = 2*rad - pos.y
            if pos.y + rad> self.height: 
                self.planets[i].velocity.y *= -self.elasticity
                pos.y = 2*(self.width-rad) - pos.y

            #Bouncing
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
            






