import time
from EdgeServer import Edge_Server
from LightDevice import Light_Device
from ACDevice import AC_Device

WAIT_TIME = 0.25  

print("\nSmart Home Simulation started.")
# Creating the edge-server for the communication with the user

edge_server_1 = Edge_Server('edge_server_1')
time.sleep(WAIT_TIME)  

# Creating the light_device
print("Intitate the device creation and registration process." )
print("\nCreating the Light devices for their respective rooms.")
light_device_ids = []
light_device_1 = Light_Device("light_1", "Kitchen")
time.sleep(WAIT_TIME)
light_device_2 = Light_Device("light_2", "BR1")
time.sleep(WAIT_TIME)
light_device_3 = Light_Device("light_3", "BR2")
time.sleep(WAIT_TIME)
light_device_4 = Light_Device("light_4", "Living")
time.sleep(WAIT_TIME)

light_device_ids.append("light_1")
light_device_ids.append("light_2")
light_device_ids.append("light_3")
light_device_ids.append("light_4")

# Creating the ac_device  
print("\nCreating the AC devices for their respective rooms. ")
ac_device_ids = []
ac_device_1 = AC_Device("ac_1", "BR1")
time.sleep(WAIT_TIME)  
ac_device_2 = AC_Device("ac_2", "BR2")
time.sleep(WAIT_TIME)  
ac_device_3 = AC_Device("ac_3", "Living")
time.sleep(WAIT_TIME)  

ac_device_ids.append("ac_1")
ac_device_ids.append("ac_2")
ac_device_ids.append("ac_3")

#Getting status of all the LIGHT devices
print("Getting status of all LIGHT devices")
for light_device_id in light_device_ids :
    edge_server_1.get_status( light_device_id )

#Getting status of all the AC devices
print("Getting status of all AC devices")
for ac_device_id in ac_device_ids :
    edge_server_1.get_status( ac_device_id )

#Getting status by device type
print("Getting status by device type")

print("Getting status of AC devices")
edge_server_1.get_Device_App_Status("AC")

print("Getting status of LIGHT devices")
edge_server_1.get_Device_App_Status("LIGHT")
#Change status of LIGHT device
#print("Getting status of all LIGHT devices")

#for light_device_id in light_device_ids :


print("\nSmart Home Simulation stopped.")
edge_server_1.terminate()
