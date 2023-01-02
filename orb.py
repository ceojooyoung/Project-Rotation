import math

#시간 관련 변수와 함수
time = 0
standard_speed = 80
speed = 80
def faster() :
    global speed
    if speed > 4 : speed -= 4
def slower() : 
    global speed
    speed += 4
def init() :
    global speed
    global standard_speed
    speed = standard_speed

#행성(+위성) 클래스 선언
class planet : 
    R=0
    T=0
    vt=0
    inner=None
    satelite = []
    x=0
    y=0
    size=0
    name = ''
    def __init__(self, name, R, T, B, size) :
        self.name=name
        self.R = R
        self.T = T
        self.size = size
        self.satelite = []
        self.vt = 3.1415926535897932384626433832795/(6*T)
        self.inner = B

    def addsatelite(self, satelite) : self.satelite.append(satelite)

    def location(self) :
        global time
        theta = time*self.vt
        self.x = math.cos(theta)*self.R
        self.y = math.sin(theta)*self.R
        if self.satelite != [] :
            for i in self.satelite :
                theta2 = time*i.vt/2
                i.x = math.cos(theta2)*i.R
                i.y = math.sin(theta2)*i.R

#행성 및 위성 정보 입력
Planet=[]
Mercury = planet('Mercury', 0.3871, 0.2408423133364, True, 49)
Planet.append(Mercury)
Venus = planet('Venus', 0.7233, 0.6151849661607202, True, 121)
Planet.append(Venus)
Earth = planet('Earth', 1, 1, True, 129)
Planet.append(Earth)
Mars = planet('Mars', 1.5237, 1.881, True, 68)
Planet.append(Mars)
Jupiter = planet('Jupiter', 5.2026, 11.862, False, 143)
Planet.append(Jupiter)
Saturn = planet('Saturn', 9.5549, 29.457, False, 121)
Planet.append(Saturn)
Moon = planet('Moon', 0.38, 0.277, True, 35)
Earth.addsatelite(Moon)
Io = planet('Io', 0.42, 0.017, False, 36)
Jupiter.addsatelite(Io)
Europa = planet('Europa', 0.67, 0.035, False, 31)
Jupiter.addsatelite(Europa)
Ganymede = planet('Ganymede', 1.07, 0.072, False, 53)
Jupiter.addsatelite(Ganymede)
Callisto = planet('Callisto', 1.88, 0.167, False, 48)
Jupiter.addsatelite(Callisto)
Titan = planet('Titan', 1.59, 0.16, False, 51)
Saturn.addsatelite(Titan)