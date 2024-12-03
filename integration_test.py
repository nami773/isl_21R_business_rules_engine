import json
import paho.mqtt.client as mqtt
import threading
import time
from main import start_communication

BROKER_HOST = "test.mosquitto.org"
PORT = 1883
TOPIC_ID = "test-1fbd893b-e02f-4b07-bc4a-001d28a52dba"
INPUT_TOPIC = f"BRE/calculateWinterSupplementInput/{TOPIC_ID}"
OUTPUT_TOPIC = f"BRE/calculateWinterSupplementOutput/{TOPIC_ID}"

# Test cases. Limited examples as this test is for integration testing
test_messages = [
    {"id": "123", "numberOfChildren": 2, "familyComposition": "single", "familyUnitInPayForDecember": True},
    {"id": "456", "numberOfChildren": 0, "familyComposition": "couple", "familyUnitInPayForDecember": False},
    {"id": "789", "numberOfChildren": 3, "familyComposition": "single", "familyUnitInPayForDecember": True},
]

expected_outputs = [
    {
        "id": "123",
        "isEligible": True,
        "baseAmount": 120.0,
        "childrenAmount": 40.0,
        "supplementAmount": 160.0,
    },
    {
        "id": "456",
        "isEligible": False,
        "baseAmount": 0.0,
        "childrenAmount": 0.0,
        "supplementAmount": 0.0,
    },
    {
        "id": "789",
        "isEligible": True,
        "baseAmount": 120.0,
        "childrenAmount": 60.0,
        "supplementAmount": 180.0,
    },
]

received_messages = []

# Publish messages to input topic
def publish_test_message(message):
    client = mqtt.Client()
    client.connect(BROKER_HOST, PORT)
    payload = json.dumps(message)
    client.publish(INPUT_TOPIC, payload)
    print(f"Published to {INPUT_TOPIC}: {payload}")
    client.disconnect()

def integration_test():
    # Start the communication process in a separate thread
    communication_thread = threading.Thread(target=start_communication, args=(TOPIC_ID,), daemon=True)
    communication_thread.start()

    time.sleep(2)

    for idx, message in enumerate(test_messages, start=1):
        print(f"Sending Test Message {idx}: {message}")
        publish_test_message(message)
        time.sleep(1)

    time.sleep(5)

    for expected in expected_outputs:
        matching_outputs = [msg for msg in received_messages if msg.get("id") == expected["id"]]
        if not matching_outputs:
            print(f"Test case with id {expected['id']} failed! No matching output received.")
            continue
        actual = matching_outputs[0]
        if actual != expected:
            print(f"Test case with id {expected['id']} failed!")
            print(f"Expected: {expected}")
            print(f"Actual:   {actual}")
        else:
            print(f"Test case with id {expected['id']} passed!")

    print("All test cases passed!")


# Start an MQTT client to subscribe to the output topic to verify response
def subscribe_to_output():
    def on_message(client, userdata, message):
        try:
            payload = json.loads(message.payload.decode("utf-8"))
            print(f"Output Received: {payload}")
            received_messages.append(payload)
        except json.JSONDecodeError:
            print("Received invalid JSON payload.")
        except Exception as e:
            print(f"Error processing message: {e}")
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER_HOST, PORT)
    client.subscribe(OUTPUT_TOPIC)
    client.loop_start()

if __name__ == "__main__":
    subscribe_to_output()
    integration_test()
