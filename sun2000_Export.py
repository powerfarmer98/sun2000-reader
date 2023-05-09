import paho.mqtt.publish as publish
topics = ["State", "CurrA", "CurrB", "CurrC", "ActPower", "Efficiency", "Temperature", "E-Total" ]
username = "mqtt"
password = "mqtt"




def sendToMqtt(data, registers):
    _data = []
    _data.append(data[1]) #Second should be state
    for pos in registers:
        if pos[0] in topics:
            place = registers.index(pos)
            _data.append(data[place+2])
    print(_data)

    for x in range(0,len(topics)):
        try:
            publish.single( topic = "SUN2000/"+topics[x], 
                            payload =  _data[x], 
                            hostname="192.168.178.154", 
                            auth = {'username':username,'password':password}
            )
        except:
            pass

def sendToMqttStandby(state = "Idle: No irradiation"):
    try:
        publish.single( topic = "SUN2000/"+topics[0], 
                        payload =  state, 
                        hostname="192.168.178.154", 
                        auth = {'username':username,'password':password}
        )
    except: 
        pass