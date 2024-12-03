# isl_21R_business_rules_engine
A solution for the coding assignment for ISL24 Full Stack Developer position

Python 3.11 with paho-mqtt installed is required to run this application.
To get started, set MQTT_TOPIC_ID on line 4 with the actual topic ID.
Then, start listening to the input topic by running:
python main.py

# Test Documentation

## Assumptions Made

- **Handling Invalid Input Formats**: There is a possibility that invalid input formats may be sent to the functions. In such cases, the functions must return appropriate error messages to inform the user of the specific validation failures.

## Tests

### Unit Tests
To run the unit tests, execute:
python unit_test.py

The unit tests focus on testing two core functions:

1. **`validate_input`**: Validates the input data for required fields and correct data types.
Test case 1: All valid inputs
Test case 2: Missing all fields
Test case 3: Incorrect data types
Test case 4: Invalid familyComposition value
Test case 5: Negative numberOfChildren
Test case 6: Empty string for id

2. **`calculate_supplement_amount`**: Calculates the supplement amount based on the validated input data.
Test case 1: Single with no children, eligible
Test case 2: Couple with no children, eligible
Test case 3: Single parent with 2 children, eligible
Test case 4: Couple with 3 children, eligible
Test case 5: Couple with 2 children, not eligible
Test case 6: Single with 0 children, not eligible

## Integration Tests
Purpose: Test the communication between the MQTT topics and the main.py application, ensuring that messages are correctly sent and received.

Because establishing communication with the provided winter supplement calculator failed, the integration tests simulate the full process by:

Sending Input Messages: Publishing test input messages to the MQTT broker's input topic.
Processing Messages: Using main.py to receive the input messages, process them, and send output messages to the output topic.
Verifying Outputs: Subscribing to the output MQTT topic to receive and verify the content of the output messages.

Note: The integration tests do not cover all possible test cases (which are handled by the unit tests). Instead, they focus on verifying the end-to-end communication and functionality between the MQTT broker and the application.