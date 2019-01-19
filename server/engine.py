import math

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
    def __init__(self, p, v, r=1, m=1):
        self.position = p
        self.velocity = v
        self.radius = r
        self.mass = m

    def intersects(self,p):
        return self.position.subtract(p.position).mod2() < math.pow(self.radius + p.radius,2)

    def accelerate(self,otherp):
        self.velocity = self.velocity.add(otherp)
        #adds to velocity vector

    def attract(self,otherp):
        between = self.position.subtract(otherp.position)
        dist = between.mod()
        force = 100*(self.mass * otherp.mass / dist ** 2)
        self.accelerate(between.scale(-force))
        otherp.accelerate(between.scale(force))
        
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
        p1 = Planet(Vector(30,150), Vector(20,100), 30)
        p2 = Planet(Vector(100,50), Vector(2,200), 50,2)
        self.planets = [p1,p2]
        self.width = w
        self.height = h

        self.clock_tick = r

    def run_loop(self):

        for i in range(len(self.planets)):
            pos = self.planets[i].position
            rad = self.planets[i].radius

            ##Boundary Checkr
            if pos.x - rad < 0: self.planets[i].velocity.x *= -1
            if pos.x + rad > self.width: self.planets[i].velocity.x *= -1
            if pos.y - rad < 0: self.planets[i].velocity.y *= -1
            if pos.y + rad > self.height: self.planets[i].velocity.y *= -1

            #Bouncing
            for j in range(i):
                if self.planets[i].intersects(self.planets[j]):
                    vi, vj = get_rebound_vectors(self.planets[i], self.planets[j])
                    self.planets[i].velocity = vi
                    self.planets[j].velocity = vj
        
            for j in range(i,len(self.planets)):
                if i!=j:
                    self.planets[i].attract(self.planets[j])

            #pos update
            self.planets[i].move(self.clock_tick)
            
            #self.planets[i].position = pos.add(self.planets[i].velocity.scale(self.clock_tick))
            






