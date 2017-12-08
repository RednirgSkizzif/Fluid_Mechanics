import matplotlib.pyplot as plt
import pdb
from math import sqrt

"""This was probably a waste of time - Dylan"""



def pressure(V,n,R,T):
    return n*R*T/V

def Force(P,A):
    return P * A

def acceleration(F,m):
    return F / m

def velocity(u,a,dt):
    return u + a * dt

def position(x,u,dt):
    return x + u * dt

def moles(n,flow,dt):
    return n + flow * dt

def Volume(x,A):
    return x * A

def flowrate(P,air_density,P_wall,A_inlet,R,T,k):
    if ( (2/air_density) * (P_wall - P) < 0):
        return 0
    return sqrt( (2/air_density) * (P_wall - P) ) * A_inlet * ( P_wall / (R*T) * k )

def propogate(step_size,num_steps,direction="up"):
#Globals
    P = 101300 # Initial pressure Pascals
    P_STP = 101300 #Standard room temp pressure
    P_wall = P_STP + 382476#68947.6 #Wall pressure 689476=100psi gauge pressure
    air_density = 1.225 # kg/m^3
    radius = 0.02 # radius of piston meters
    A = 3.14 * radius**2# Area of piston face
    A_inlet = 3.14 * 0.003175**2 # cross sectional area of inlet valve
    k = 0.03 #empiracal constant from fluid denamics through oriface
    x = 0.010 # intial length meters
    V = x * A #inital length times area
    R = 8.314#J/ mol K
    T = 273#Kelvin
    n = P * V / ( R * T ) # moles
    m = 0.5 #mass of piston kg
    u = 0.0 # velocity
    a = 0.0 # acceleration
    F = 0.0 # force
    friction = 1 # frictional losses
    #flow = 1 * 0.0224 # Liters per second times moles in a liter
    impact_point = 0.050 # x distance that hammer makes impact
    strike=0 # The hammer has not yet struck the table
    
    P_list = [] # for plotting
    pos_list = []
    times = []
    vel_list = []
    moles_list = []
    a_list = []
    vol_list = []
    flow_list = []
    
    #Algorithm Engine
    for dt in range(1,num_steps):
        #pdb.set_trace()
        flow = flowrate(P,air_density,P_wall,A_inlet,R,T,k)#calculate the flow rate
        n = moles(n,flow,step_size) #update num moles
        P = pressure(V,n,R,T) # update pressure
        F = Force(P,A) - (P_STP * A) - friction # subtract room air pressure and estimate friction
        a = acceleration(F,m) #calculate a
        u = velocity(u,a,step_size ) #update velocity
        x = position(x,u,step_size ) #update position
        V = Volume(A,x) # calculate V
        
        if(x > impact_point ):
            energy = 0.5 * m * u*u
            if not strike:
                print("Energy of impact = " + str(energy) +"Joules")
                strike=1
            u = 0
            a = 0
            x = impact_point
    #End Engine
    
        #Gather for plotting
        flow_list.append(flow)
        moles_list.append(n)
        times.append(dt)
        P_list.append(P)
        a_list.append(a)
        vel_list.append(u)
        pos_list.append(x)
        vol_list.append(V)
        #print("timestep = " + str(dt))
        #print("position = " + str(x))
        #print("Presure = " + str(P))
    #Plots
    plt.subplot(6, 1, 1)
    plt.plot(times, P_list, 'ko-')
    plt.title('Time evolution of piston')
    plt.ylabel('Pressure in Pascals')
    
    plt.subplot(6, 1, 2)
    plt.plot(times, flow_list, 'y-')
    plt.ylabel('flow in moles/sec')

    plt.subplot(6, 1, 3)
    plt.plot(times, moles_list, 'y.-')
    plt.ylabel('gas in moles')

    plt.subplot(6, 1, 4)
    plt.plot(times, a_list, 'ko-')
    plt.ylabel('acceleration m/ss')

    plt.subplot(6, 1, 5)
    vel_average = sum(vel_list)/len(vel_list)
    #plt.plot(times, vel_list, [-10,num_steps],[vel_average,vel_average] ,'b.-')
    plt.plot(times, vel_list ,'b.-')
    plt.ylabel('Velocity m/s')

    plt.subplot(6, 1, 6)
    table_height = 0.05
    plt.plot(times, pos_list,[-10,num_steps],[table_height,table_height], 'r-')
    plt.ylabel('position m')
    
#plt.subplot(7, 1, 7)
#    plt.plot(times, vol_list, 'r.-')
#    plt.xlabel('time (millisecond)')
#    plt.ylabel('Volume m^3')

    plt.show()

#main loop
state ={}

propogate(0.001,100,direction="up") #Step size and num_steps







