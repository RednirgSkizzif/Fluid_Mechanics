import matplotlib.pyplot as plt
import pdb

#"This is probably a waste of time - Dylan"



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


def propogate(step_size,num_steps):
#Globals
    P = 101300 # Initial pressure Pascals
    P_STP = 101300 #Standard room temp pressure
    radius = 0.050 # radius of piston meters
    A = 3.14 * (radius )**2# Area of piston face
    x = 0.010 # intial length meters
    V = x * A #inital length times area
    R = 8.314#J/ mol K
    T = 273#Kelvin
    n = P * V / ( R * T ) # moles
    m = 0.5 #mass of piston
    u = 0.0 # velocity
    a = 0.0 # acceleration
    F = 0.0 # force
    friction = 1#pseduo frictional force
    flow = 1 * 0.0224 # Liters per second times moles in a liter
    
    P_list = [] # for plotting
    pos_list = []
    times = []
    vel_list = []
    moles_list = []
    a_list = []
    
    #Algorithm Engine
    for dt in range(1,num_steps):
        #pdb.set_trace()
        n = moles(n,flow,step_size)
        P = pressure(V,n,R,T)
        F = Force(P,A) - (P_STP * A) - friction # subtract air pressure and estimate friction
        a = acceleration(F,m)
        u = velocity(u,a,step_size )
        x = position(x,u,step_size )
        V = Volume(A,x)
    #End Engine
    
        #Gather for plotting
        moles_list.append(n)
        times.append(dt)
        P_list.append(P)
        a_list.append(a)
        vel_list.append(u)
        pos_list.append(x)
        #print("timestep = " + str(dt))
        #print("position = " + str(x))
        #print("Presure = " + str(P))
    #Plots
    plt.subplot(5, 1, 1)
    plt.plot(times, P_list, 'ko-')
    plt.title('Time evolution of piston')
    plt.ylabel('Pressure in Pascals')

    plt.subplot(5, 1, 2)
    plt.plot(times, moles_list, 'y.-')
    plt.ylabel('gas in moles')

    plt.subplot(5, 1, 3)
    plt.plot(times, a_list, 'ko-')
    plt.ylabel('acceleration m/ss')

    plt.subplot(5, 1, 4)
    plt.plot(times, vel_list, 'b.-')
    plt.ylabel('Velocity m/s')

    plt.subplot(5, 1, 5)
    plt.plot(times, pos_list, 'r.-')
    plt.xlabel('time (millisecond)')
    plt.ylabel('position m')

    plt.show()

#main loop
propogate(0.001,1000) #STtep size and num_steps






