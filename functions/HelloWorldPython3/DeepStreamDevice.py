from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder

def device_subscribe(my_topic):
    # Subscribe
    print("DeepStream Device Subscribing to topic '{}'...".format(my_topic))
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=my_topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)


def on_message_received(topic, payload, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload))