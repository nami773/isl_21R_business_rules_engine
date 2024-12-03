import json
import paho.mqtt.client as mqtt

MQTT_TOPIC_ID = "test-1fbd893b-e02f-4b07-bc4a-001d28a52dba"
BROKER_HOST = "test.mosquitto.org"
PORT = 1883

client = mqtt.Client()
client.enable_logger()


def validate_input(input_data):
    reasons_of_error = []
    if type(input_data.get("id")) != str or not input_data.get("id"):
        reasons_of_error.append("'id' field of type string is required.")

    if (
        type(input_data.get("numberOfChildren")) != int
        or input_data.get("numberOfChildren") < 0
    ):
        reasons_of_error.append(
            "'numberOfChildren' field of type positive integer is required."
        )

    if input_data.get("familyComposition") not in ["single", "couple"]:
        reasons_of_error.append(
            "'familyComposition' field must be present and should be either 'single' or 'couple'."
        )

    if type(input_data.get("familyUnitInPayForDecember")) != bool:
        reasons_of_error.append(
            "'familyUnitInPayForDecember' field must be present and should be a boolean."
        )

    return reasons_of_error


def calculate_supplement_amount(input_data):
    unique_id = input_data["id"]
    is_eligible = input_data["familyUnitInPayForDecember"]
    number_of_children = input_data["numberOfChildren"]
    family_composition = input_data["familyComposition"]

    base_amount = 0.0
    children_amount = 0.0

    if is_eligible:
        if family_composition == "single" and number_of_children == 0:
            base_amount = 60.0
        else:
            base_amount = 120.0
            children_amount = 20.0 * number_of_children

    supplement_amount = base_amount + children_amount

    result = {
        "id": unique_id,
        "isEligible": is_eligible,
        "baseAmount": base_amount,
        "childrenAmount": children_amount,
        "supplementAmount": supplement_amount,
    }

    return result


def start_communication(topic_id):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT broker successfully for {topic_id}.")
        else:
            print(f"Failed to connect with result code {rc}")

    def on_disconnect(client, userdata, rc):
        print(f"Disconnected from broker for {topic_id}.")

    def on_message(client, userdata, message):
        print("message received")
        try:
            payload = json.loads(message.payload.decode("utf-8"))
            output_topic = f"BRE/calculateWinterSupplementOutput/{topic_id}"
            errors = validate_input(payload)
            if errors:
                response = {"errors": errors}
            else:
                response = calculate_supplement_amount(payload)
            client.publish(output_topic, json.dumps(response))
            print(f"Published to {output_topic}: {json.dumps(response)}")
        except json.JSONDecodeError:
            print("Received invalid JSON payload.")
        except Exception as e:
            print(f"Error processing message: {e}")

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(BROKER_HOST, PORT)
    input_topic = f"BRE/calculateWinterSupplementInput/{topic_id}"
    client.subscribe(input_topic)
    print(f"Listening for input messages on topic: {input_topic}...")
    client.loop_forever()


if __name__ == "__main__":
    start_communication(MQTT_TOPIC_ID)
