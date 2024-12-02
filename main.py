def validate_input(input_data):
    reasons_of_error = []
    if type(input_data.get("id")) != str:
        reasons_of_error.append("'id' field of type string is required.")

    if type(input_data.get("numberOfChildren")) != int:
        reasons_of_error.append("'numberOfChildren' field of type integer is required.")

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
    unique_id = input_data.get("id", "")
    is_eligible = input_data.get("familyUnitInPayForDecember", False)
    number_of_children = input_data.get("numberOfChildren", 0)
    family_composition = input_data.get("familyComposition", "").lower()

    base_amount = 0.0
    children_amount = 0.0

    if is_eligible:
        if family_composition == "single" and number_of_children == 0:
            base_amount = 60.0
        elif family_composition == "couple" and number_of_children == 0:
            base_amount = 120.0
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


def main(input_data):
    errors = validate_input(input_data)
    if errors:
        return {"errors": errors}
    return calculate_supplement_amount(input_data)
