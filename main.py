import time
import json
import sys
from EdgeServer import Edge_Server
from LightDevice import Light_Device
from ACDevice import AC_Device

WAIT_TIME = 0.25  
f = open('output.txt','w')
sys.stdout = f

print("\nSmart Home Simulation started.")
# Creating the edge-server for the communication with the user

edge_server_1 = Edge_Server('edge_server_1')
time.sleep(WAIT_TIME)  

# Creating the light_device
print("********************Intitate the device creation and registration process.********************\n\n")
print("##########Creating the Light devices for their respective rooms.##########\n")
light_device_ids = []
light_device_1 = Light_Device("light_1", "Kitchen")
time.sleep(WAIT_TIME)
light_device_2 = Light_Device("light_2", "BR1")
time.sleep(WAIT_TIME)
light_device_3 = Light_Device("light_3", "BR2")
time.sleep(WAIT_TIME)
light_device_4 = Light_Device("light_4", "Living")
time.sleep(WAIT_TIME)

#ID list for LIGHT
light_device_ids.append("light_1")
light_device_ids.append("light_2")
light_device_ids.append("light_3")
light_device_ids.append("light_4")
print("----------------------------------------------------------------------\n")

# Creating the ac_device  
print("##########Creating the AC devices for their respective rooms.##########\n")
ac_device_ids = []
ac_device_1 = AC_Device("ac_1", "BR1")
time.sleep(WAIT_TIME)  
ac_device_2 = AC_Device("ac_2", "BR2")
time.sleep(WAIT_TIME)  
ac_device_3 = AC_Device("ac_3", "Living")
time.sleep(WAIT_TIME)  
print("********************************************************************************\n\n")

#ID list for AC
ac_device_ids.append("ac_1")
ac_device_ids.append("ac_2")
ac_device_ids.append("ac_3")

#ID list for Rooms
room_ids = []
room_ids.append("Living")
room_ids.append("BR1")
room_ids.append("BR2")
room_ids.append("Kitchen")

print("********************Getting all Registered Devices********************\n\n")
print(edge_server_1.get_registered_device_list())
print("----------------------------------------------------------------------\n")

print("********************Getting Current Status by Devices********************\n\n")
#Getting status of all the LIGHT devices
print("##########Getting status of all LIGHT devices##########\n")
for light_device_id in light_device_ids :
    edge_server_1.get_status( light_device_id )
print("----------------------------------------------------------------------\n")
#Getting status of all the AC devices
print("##########Getting status of all AC devices##########\n")
for ac_device_id in ac_device_ids :
    edge_server_1.get_status( ac_device_id )
print("********************************************************************************\n\n")

#Getting status by device type
print("********************Getting Status by Device Type********************\n\n")
print("##########Getting status of AC devices##########\n")
edge_server_1.get_Device_App_Status("AC")
print("----------------------------------------------------------------------\n")
print("##########Getting status of LIGHT devices##########\n")
edge_server_1.get_Device_App_Status("LIGHT")

#Getting status by room type
print("********************Getting Status by Room Type********************\n\n")
for room_id in room_ids :
    edge_server_1.get_Room_App_Status(room_id)
print("********************************************************************************\n\n")
print("##########Getting status of LIGHT devices##########\n")

#Changing the status and value, i.e. Temperature or Intensity of Devices
print("********************Changing Status of Devices********************\n\n")
print("##########Changing status of LIGHT devices##########\n")
data_in_LIGHT = {}
data_in_LIGHT["Status"] = "ON"
data_in_LIGHT["Intensity"] = 0
edge_server_1.set("light_1",json.dumps(data_in_LIGHT))
data_in_LIGHT["Intensity"] = 1
edge_server_1.set("light_2",json.dumps(data_in_LIGHT))
data_in_LIGHT["Intensity"] = 2
edge_server_1.set("light_3",json.dumps(data_in_LIGHT))
data_in_LIGHT["Intensity"] = 3
edge_server_1.set("light_4",json.dumps(data_in_LIGHT))

print("##########Changing status of AC devices##########\n")
data_in_AC = {}
data_in_AC["Status"] = "ON"
data_in_AC["Temperature"] = 20
edge_server_1.set("ac_1",json.dumps(data_in_AC))
data_in_AC["Temperature"] = 21
edge_server_1.set("ac_2",json.dumps(data_in_AC))
data_in_AC["Temperature"] = 19
edge_server_1.set("ac_3",json.dumps(data_in_AC))
print("********************************************************************************\n\n")

#Getting status of all the LIGHT devices after changes
print("********************Changing Status of Devices after changes********************\n\n")
print("##########Getting status of all LIGHT devices after changes##########\n")
for light_device_id in light_device_ids :
    edge_server_1.get_status( light_device_id )
print("----------------------------------------------------------------------\n")
#Getting status of all the AC devices after changes
print("##########Getting status of all AC devices after changes##########\n")
for ac_device_id in ac_device_ids :
    edge_server_1.get_status( ac_device_id )
print("********************************************************************************\n\n")
print("\nSmart Home Simulation stopped.")
edge_server_1.terminate()
