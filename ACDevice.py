
import json
import paho.mqtt.client as mqtt


HOST = "localhost"
PORT = 1883
    
class AC_Device():
    
    _MIN_TEMP = 18  
    _MAX_TEMP = 32  

    def __init__(self, device_id, room):
        
        self._device_id = device_id
        self._room_type = room
        self._temperature = 22
        self._device_type = "AC"
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)  
        self.client.on_connect = self._on_connect  
        self.client.on_message = self._on_message  
        self.client.on_disconnect = self._on_disconnect  
        self.client.connect(HOST, PORT, keepalive=60)  
        self.client.loop_start()  
        self._register_device(self._device_id, self._room_type, self._device_type)
        self._switch_status = "OFF"

    def _get_id(self):
        return "D2E/AC/{0}/{1}".format(self._room_type,self._device_id)

    def _get_header(self):
        data = {}
        data["Device_ID"] = self._device_id
        data["Room_Type"] = self._room_type
        data["Device_Type"] = self._device_type
        return data

    # calling registration method to register the device
    def _register_device(self, device_id, room_type, device_type):
        print("DEVICE : Register for AC device called")
        data = self._get_header()
        data["Request_Type"] = "Register"
        data_out = json.dumps(data)
        self.client.publish(self._get_id(),data_out,2)

    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):
        if result_code == 0 :
            self.client.subscribe(("E2D/AC/{0}/{1}".format(self._room_type,self._device_id),2))

    def _on_disconnect(self, client, userdata, rc):
        if ( rc == 0 ) :
            self.client.disconnect()

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg): 
        data_in = json.loads(msg.payload)
        if "Registration_Status" in data_in :
            self._device_registration_flag = data_in["Registration_Status"]
            if self._device_registration_flag :
                print("DEVICE : AC-DEVICE is registered. Registration status for {0} is TRUE".format(self._device_id))
            else:
                print("DEVICE : AC-DEVICE did not register. Registration status for {0} is FALSE".format(self._device_id))
        elif "Status" in data_in :
            if data_in["Status"] == "SET" :
                self._set_switch_status(data_in["Device_Status"])
                self._set_temperature(data_in["Temperature"])
                print("DEVICE : Status for AC-DEVICE with id {} for room {} is set to following value".format(self._device_id,self._room_type))
                print("DEVICE : Switch status : {}".format(self._get_switch_status()))
                print("DEVICE : Temperature : {}".format(self._get_temperature()))
            elif data_in["Status"] == "GET" :
                data = self._get_header()
                data["Request_Type"] = "Status"
                data["Status"] = self._get_switch_status()
                data["Temperature"] = self._get_temperature()
                data_out = json.dumps(data)
                self.client.publish(self._get_id(),data_out,2)
        
    # Getting the current switch status of devices 
    def _get_switch_status(self):
        return self._switch_status

    # Setting the the switch of devices
    def _set_switch_status(self, switch_state):
        onstr = "ON"
        offstr = "OFF"
        if switch_state == onstr.lower() or switch_state == onstr.upper() :
            self._switch_status = onstr
        elif switch_state == offstr.lower() or switch_state == offstr.upper() :
            self._switch_status = offstr
        else:
            print("DEVICE : Faulty status value, status value not changed")

    # Getting the temperature for the devices
    def _get_temperature(self):
        return self._temperature

    # Setting up the temperature of the devices
    def _set_temperature(self, temperature):
        if temperature >= self._MIN_TEMP or temperature <= self._MAX_TEMP :
            self._temperature = temperature
        elif temperature < self._MIN_TEMP:
            self._temperature = self._MIN_TEMP
        else:
            self._temperature = self._MAX_TEMP
    
