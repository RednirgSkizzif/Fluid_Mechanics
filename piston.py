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

def flowrate_in(P,air_density,P_wall,A_inlet,R,T,k):
    if ( (P_wall - P) < 0):#This will be replaced by full emprical equation
        return sqrt( (2/air_density) * (P - P_wall) ) * A_inlet * ( P / (R*T) * k ) * -1.0
    return sqrt( (2/air_density) * (P_wall - P) ) * A_inlet * ( P_wall / (R*T) * k )

def flowrate_out(P,air_density,P_STP,A_inlet,R,T,k):
    if ( (P - P_STP) < 0):#This will be replaced by full emprical equation
        return sqrt( (2/air_density) * (P_STP - P) ) * A_inlet * ( P_STP / (R*T) * k )
    return sqrt( (2/air_density) * (P - P_STP) ) * A_inlet * ( P / (R*T) * k ) * -1.0 #negative sign to represent moles leaving

def update_state_up(step_size, s):
    s["flow_1"] = flowrate_in(s["P_1"],s["air_density"],s["P_wall"],s["A_inlet"],s["R"],s["T"],s["k"])#calculate the flow rate
    s["flow_2"] = flowrate_out(s["P_2"],s["air_density"],s["P_STP"],s["A_inlet"],s["R"],s["T"],s["k"])#calculate the flow rate
    s["n_1"] = moles(s["n_1"],s["flow_1"],step_size) #update num moles
    s["n_2"] = moles(s["n_2"],s["flow_2"],step_size) #update num moles
    s["P_1"] = pressure(s["V_1"],s["n_1"],s["R"],s["T"]) # update pressure
    s["P_2"] = pressure(s["V_2"],s["n_2"],s["R"],s["T"]) # update pressure
    s["F_1"] = Force(s["P_1"],s["A"]) # subtract room air pressure and estimate friction
    s["F_2"] = Force(s["P_2"],s["A"]) # subtract room air pressure and estimate friction
    s["a"] = acceleration(s["F_1"] - s["F_2"] + s["impact"]  - s["friction_loss"] ,s["m"]) #calculate a
    s["u"] = velocity(s["u"],s["a"],step_size ) #update velocity
    s["x"] = position(s["x"],s["u"],step_size ) #update position

    s["V_1"] = Volume(s["A"],s["x"]) # calculate V
    s["V_2"] = Volume(s["A"],s["x_max"]-s["x"]+s["x_min"]) # calculate V
    s["time"] = s["time"]+step_size
    
    if s["x"] >= s["x_max"] :
        s["impact"] = - s["impulse_k"] * (s["x"]-s["x_max"])
        s["transfer"] = s["a"] / (s["mass_table"]/s["m"])
    elif s["x"] <= s["x_min"]:
        s["impact"] = - s["impulse_k"] * (s["x"]-s["x_min"])
        s["transfer"] = s["a"] / (s["mass_table"]/s["m"])
    else:
        s["transfer"] = 0.0
        s["impact"] = 0.0

    return s

def update_state_down(step_size, s):
    s["flow_1"] = flowrate_out(s["P_1"],s["air_density"],s["P_STP"],s["A_inlet"],s["R"],s["T"],s["k"])#calculate the flow rate
    s["flow_2"] = flowrate_in(s["P_2"],s["air_density"],s["P_wall"],s["A_inlet"],s["R"],s["T"],s["k"])#calculate the flow rate
    s["n_1"] = moles(s["n_1"],s["flow_1"],step_size) #update num moles
    s["n_2"] = moles(s["n_2"],s["flow_2"],step_size) #update num moles
    s["P_1"] = pressure(s["V_1"],s["n_1"],s["R"],s["T"]) # update pressure
    s["P_2"] = pressure(s["V_2"],s["n_2"],s["R"],s["T"]) # update pressure
    s["F_1"] = Force(s["P_1"],s["A"]) # subtract room air pressure and estimate friction
    s["F_2"] = Force(s["P_2"],s["A"]) # subtract room air pressure and estimate friction
    s["a"] = acceleration(s["F_1"] - s["F_2"] + s["impact"] - s["friction_loss"],s["m"]) #calculate a
    s["u"] = velocity(s["u"],s["a"],step_size ) #update velocity
    s["x"] = position(s["x"],s["u"],step_size ) #update position

    s["V_1"] = Volume(s["A"],s["x"]) # calculate V
    s["V_2"] = Volume(s["A"],s["x_max"]-s["x"]+s["x_min"]) # calculate V
    s["time"] = s["time"]+step_size
    
    if s["x"] >= s["x_max"] :
        s["impact"] = - s["impulse_k"] * (s["x"]-s["x_max"])
        s["transfer"] = s["a"] / (s["mass_table"]/s["m"])
    elif s["x"] <= s["x_min"]:
        s["impact"] = - s["impulse_k"] * (s["x"]-s["x_min"])
        s["transfer"] = s["a"] / (s["mass_table"]/s["m"])
    else:
        s["transfer"] = 0.0
        s["impact"] = 0.0
    return s


def propogate(step_size,num_steps,num_cycles,state_vector):
#Globals

    P1_list = [] # for plotting
    pos_list = []
    times = []
    vel_list = []
    moles1_list = []
    a_list = []
    flow1_list = []
    P2_list = []
    moles2_list = []
    flow2_list = []
    transfer_a = []
    vol_2 = []
    pressure = state_vector["P_wall"]
    
    for cycle in range(0,num_cycles):
      #Algorithm Engine
      if cycle == 0:
          state_vector["P_wall"] = 0.5 * pressure
      else:
          state_vector["P_wall"] = pressure
      
      for dt in range(1,num_steps):
          state_vector=  update_state_up(step_size,state_vector)
        
          #Gather for plotting
          flow1_list.append(state_vector["flow_1"])
          flow2_list.append(state_vector["flow_2"])
          moles1_list.append(state_vector["n_1"])
          moles2_list.append(state_vector["n_2"])
          times.append(state_vector["time"])
          P1_list.append(state_vector["P_1"])
          P2_list.append(state_vector["P_2"])
          a_list.append(state_vector["a"])
          vel_list.append(state_vector["u"])
          pos_list.append(state_vector["x"])
          transfer_a.append(state_vector["transfer"]/9.8)
          vol_2.append(state_vector["V_2"])
    
      for dt in range(1,num_steps):
          state_vector= update_state_down(step_size,state_vector)
        
          flow1_list.append(state_vector["flow_1"])
          flow2_list.append(state_vector["flow_2"])
          moles1_list.append(state_vector["n_1"])
          moles2_list.append(state_vector["n_2"])
          times.append(state_vector["time"])
          P1_list.append(state_vector["P_1"])
          P2_list.append(state_vector["P_2"])
          a_list.append(state_vector["a"])
          vel_list.append(state_vector["u"])
          pos_list.append(state_vector["x"])
          transfer_a.append(state_vector["transfer"]/9.8)
          vol_2.append(state_vector["V_2"])



#for x in pos_list:
#  print(x)
    #Plots
    plt.subplot(6, 2, 1)
    plt.plot(times, P1_list, 'ko-')
    plt.title('Time evolution of bottom of piston')
    plt.ylabel('Pressure Pascals')
    
    plt.subplot(6, 2, 2)
    plt.plot(times, P2_list, 'ko-')
    plt.title('Time evolution of top of piston')
    plt.ylabel('Pressure Pascals')
    
    plt.subplot(6, 2, 3)
    plt.plot(times, flow1_list, 'y-')
    plt.ylabel('moles/sec')
    
    plt.subplot(6, 2, 4)
    plt.plot(times, flow2_list, 'y-')
    plt.ylabel('moles/sec')

    plt.subplot(6, 2, 5)
    plt.plot(times, moles1_list, 'y.-')
    plt.ylabel('gas moles')
    
    plt.subplot(6, 2, 6)
    plt.plot(times, moles2_list, 'y.-')
    plt.ylabel('gas moles')

    plt.subplot(6, 2, 7)
    plt.plot(times, a_list, 'ko-')
    plt.ylabel(' m/s**2')
    
    plt.subplot(6, 2, 8)
    plt.plot(times, transfer_a, 'ko-')
    plt.ylabel("transfer g's")

    plt.subplot(6, 2, 9)
    vel_average = sum(vel_list)/len(vel_list)
    #plt.plot(times, vel_list, [-10,num_steps],[vel_average,vel_average] ,'b.-')
    plt.plot(times, vel_list ,'b.-')
    plt.ylabel(' m/s')

    plt.subplot(6, 2, 11)
    table_height = 0.05
    plt.plot(times, pos_list, 'r-')
    plt.ylabel('position m')
    tot = 0
    for each in transfer_a:
        print(each)
        tot = tot + each**2
    print("The grms is : " + str(sqrt( tot / (len(transfer_a) * step_size) ) ) )
    plt.show()

#main loop
gauge_pressure = 112476 #Pressure supplied to system
mass = 0.5#mass of cylinder
r = 0.01#radius of cylinder
cycles = 5

state_vector ={
    "P_1":101300,#Pressure in Pascals
    "P_STP":101300,#Standard Temp and Pressure P
    "P_2": 101300,#Pressure of seond piston cavity
    "air_density":1.225,#Desnity of air in kg/m^3
    "radius": r,#radius of cylinder in meters
    "A_inlet":3.14 * 0.003175**2,#Cross sectional area of inlet, meters
    "k":0.01,#imperical flow resistance
    "x_max":0.020,#length at which piston hits table
    "x_min":0.005,#Min position of piston
    "R":8.314,#Ideal Gas Const J/mol K
    "T":273,#Temp in Kelvin
    "m":mass,#mass of cylinder in kg
    "u":0.0,#velocity m/s
    "a":0.0,#Acceleration m/ss
    "F_1":0.0,#Force applied to piston, N
    "F_2":0.0,#Force top side of piston
    "friction_loss":1.0,#empirical friction force of piston
    "flow_1":0.0, #Air flow in moles/s this will be function of pressure differential
    "time":0.0, #Global time variables sec
    "impact": 0.0, #Force due t impact Newtons
    "impulse_k": 500000, #emprical impulse coefficient
    "mass_table": 10.0, #mass of table
    "transfer": 0.0, #Energy transfered to the table
    "momentum_loss_factor":1.0 #emprical factor to gauge inefficency (sound, heat loss)
}
state_vector.update({
    "P_wall":state_vector["P_STP"] + gauge_pressure,#Pressure of regulator
    "A":3.14 * state_vector["radius"]**2,#Cross sectional area of cylinder
    "x":state_vector["x_min"],#Postion of piston meters
                    })
state_vector.update({
    "V_1":state_vector["A"] * state_vector["x"],
    "V_2":state_vector["A"] * (state_vector["x_max"]-state_vector["x"])
                    })
state_vector.update({
    "n_1":(state_vector["P_1"] * state_vector["V_1"]) / (state_vector["R"] * state_vector["T"]),
    "n_2":(state_vector["P_2"] * state_vector["V_2"]) / (state_vector["R"] * state_vector["T"])
                    })

propogate(0.001,500,cycles,state_vector) #Step size and num_steps







