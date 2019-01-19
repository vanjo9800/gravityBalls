import math
import json

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

    def mod2(self):
        return self.x*self.x + self.y*self.y

    def mod(self):
        return math.sqrt(self.mod2())

    def normalised(self):
        return Vector(self.x,self.y).scale(1/self.mod())

class Planet:
    def __init__(self, p, v, nid, r=1, m=1):
        self.position = p
        self.velocity = v
        self.radius = r
        self.mass = m
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
        force = 5000*((self.mass * otherp.mass / dist ** 2)**1)
        self.accelerate(between.scale(-force),clock_tick)
        otherp.accelerate(between.scale(force),clock_tick)
        #Scale force to clock tick?
        
    def move(self,clock_tick):
        self.position = self.position.add(self.velocity.scale(clock_tick))

def get_rebound_vectors(p1, p2):
    n = p2.position.subtract(p1.position).normalised()
    u1 = p1.velocity.dot(n)
    u2 = p2.velocity.dot(n)
    v1 = ((p1.mass-p2.mass)*u1 + 2*p2.mass*u2) / (p1.mass+p2.mass)
    v2 = ((p2.mass-p1.mass)*u2 + 2*p1.mass*u1) / (p1.mass+p2.mass)
    return (p1.velocity.subtract(n.scale(u1-v1)), p2.velocity.subtract(n.scale(u2-v2)))

class Universe:
    def __init__(self, w, h, r):
        p1 = Planet(Vector(30,150), Vector(20,100),0, 30,0)
        p2 = Planet(Vector(100,50), Vector(2,200), 1, 50,2)
        p3 = Planet(Vector(300,50), Vector(2,200), 2, 50,2)
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

    def run_loop(self):

        for i in range(len(self.planets)):
            pos = self.planets[i].position
            rad = self.planets[i].radius
            elasticity = self.elasticity

            ##Boundary Checkr
            if pos.x - rad< 0: 
                self.planets[i].velocity.x *= -elasticity
                pos.x = 2*rad - pos.x
            if pos.x + rad> self.width: 
                self.planets[i].velocity.x *= -elasticity
                pos.x = 2*(self.width-rad) - pos.x
            if pos.y - rad< 0: 
                self.planets[i].velocity.y *= -elasticity
                pos.y = 2*rad - pos.y
            if pos.y + rad> self.height: 
                self.planets[i].velocity.y *= -elasticity
                pos.y = 2*(self.width-rad) - pos.y

            #Bouncing
            for j in range(i):
                if self.planets[i].intersects(self.planets[j]):
                    firstone = self.planets[i]
                    secondone = self.planets[j]
                    vi, vj = get_rebound_vectors(firstone,secondone)
                    elasticity = firstone.elasticity * secondone.elasticity
                    firstone.velocity = vi.scale(elasticity)
                    secondone.velocity = vj.scale(elasticity)

                    ##Overlapping fix
                    dist = firstone.position.subtract(secondone.position).mod()
                    overlap = 0.2*(firstone.radius+secondone.radius-dist+1)
                    firstone.position.add(firstone.velocity.scale(-1).scale(overlap))
                    secondone.position.add(secondone.velocity.scale(-1).scale(overlap))

                if (i!=j):
                    self.planets[i].attract(self.planets[j],self.clock_tick)

            #pos update
            self.planets[i].move(self.clock_tick)
            
            #self.planets[i].position = pos.add(self.planets[i].velocity.scale(self.clock_tick))
            






