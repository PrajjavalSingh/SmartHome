
import json
import time
import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883     
WAIT_TIME = 0.25  

class Edge_Server:
    
    def __init__(self, instance_name):
        
        self._instance_id = instance_name
        self.client = mqtt.Client(self._instance_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()
        self._registered_list = []
        self._registered_device_data = {}

    # Terminating the MQTT broker and stopping the execution
    def terminate(self):
        self.client.disconnect()
        self.client.loop_stop()

    # Connect method to subscribe to various topics.     
    def _on_connect(self, client, userdata, flags, result_code):
        if result_code == 0 :
            print("EdgeServer : Connection successful")
            self.client.subscribe(("D2E/LIGHT/#",2))
            self.client.subscribe(("D2E/AC/#",2))
        elif result_code == 1 :
            print("EdgeServer : Connection refused – incorrect protocol version")
        elif result_code == 2 :
            print("EdgeServer : Connection refused – invalid client identifier")
        elif result_code == 3 :
            print("EdgeServer : Connection refused – server unavailable")        
        elif result_code == 4 :
            print("EdgeServer : Connection refused – bad username or password")
        elif result_code == 5 :
            print("EdgeServer : Connection refused – not authorised")
        else :
            print("EdgeServer : Currently unused")

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        data_in = json.loads(msg.payload)
        req_type = data_in["Request_Type"]
        device_type = data_in["Device_Type"]
        room_type = data_in["Room_Type"]
        device_id = data_in["Device_ID"]
        data = {}
        if req_type == "Register" :
            self._registered_list.append(data_in["Device_ID"])
            dvcdata = {}
            dvcdata["Room_Type"] = room_type
            dvcdata["Device_Type"] = device_type
            self._registered_device_data[device_id] = dvcdata
            print("EdgeServer : Registration for {} device in {} successful, Device ID : {}".format(device_type,room_type,device_id))
            data["Registration_Status"] = True
            data_out = json.dumps(data)
            self.client.publish(self._get_id(device_type,room_type,device_id),data_out,2)
        elif req_type == "Status" :
            status = data_in["Status"]
            if device_type == "AC" :
                temperature = data_in["Temperature"]
                print("EdgeServer : Status for AC device in {}, Device ID : {}, Status : {}, Temperature : {}".format(room_type,device_id,status,temperature))
            else:
                intensity = data_in["Intensity"]
                print("EdgeServer : Status for LIGHT device in {}, Device ID : {}, Status : {}, Intensity : {}".format(room_type,device_id,status,intensity))
    
    # Returning the current registered list
    def get_registered_device_list(self):
        return self._registered_list


    def _get_id(self,device_type,room_type,device_id):
        return "E2D/{0}/{1}/{2}".format(device_type,room_type,device_id)

    def _get_Data_For_DvcID(self, device_id):
        dvcdata = self._registered_device_data[device_id]
        return dvcdata["Device_Type"], dvcdata["Room_Type"]

    # Getting the status for the connected devices
    def get_status(self,device_id):
        data = {}
        data["Status"] = "GET"
        data_out = json.dumps(data)
        device_type, room_type = self._get_Data_For_DvcID(device_id)
        print("EdgeServer : Getting status for {0} for device type {1} for room {2}".format(device_id,device_type,room_type))
        self.client.publish(self._get_id(device_type,room_type,device_id),data_out,2)
        time.sleep(WAIT_TIME)
        print("\n")

    
    def get_Room_App_Status(self,room_type):
        for dvcid in self._registered_list :
            dvctyp,dvcroom = self._get_Data_For_DvcID(dvcid)
            if dvcroom == room_type:
                self.get_status( dvcid )

    def get_Device_App_Status(self,device_type):
        for dvcid in self._registered_list :
            dvctyp,dvcroom = self._get_Data_For_DvcID(dvcid)
            if dvctyp == device_type:
                self.get_status( dvcid )

    # Controlling and performing the operations on the devices
    # based on the request received
    def set(self,device_id,payload):
        data = json.loads(payload)
        data["Status"] = "SET"
        data_out = json.dumps(data)
        device_type, room_type = self._get_Data_For_DvcID(device_id)
        print("EdgeServer : Setting status for {0} for device type {1} for room {2}".format(device_id,device_type,room_type))
        self.client.publish(self._get_id(device_type,room_type,device_id),data_out,2)
        time.sleep(WAIT_TIME)