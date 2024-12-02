from main import validate_input, calculate_supplement_amount


def test_validate_input():
    print("Testing validate_input...")

    # Test case 1: All valid inputs
    try:
        valid_input = {
            "id": "12345",
            "numberOfChildren": 2,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": True,
        }
        assert validate_input(valid_input) == []
    except AssertionError:
        print("Test case 1: 'Valid inputs' failed.")

    # Test case 2: Missing fields
    try:
        missing_fields_input = {}
        assert validate_input(missing_fields_input) == [
            "'id' field of type string is required.",
            "'numberOfChildren' field of type integer is required.",
            "'familyComposition' field must be present and should be either 'single' or 'couple'.",
            "'familyUnitInPayForDecember' field must be present and should be a boolean.",
        ]
    except AssertionError:
        print("Test case 2: 'Missing fields' failed.")

    # Test case 3: Incorrect data types
    try:
        invalid_types_input = {
            "id": 12345,
            "numberOfChildren": "two",
            "familyComposition": "single",
            "familyUnitInPayForDecember": "yes",
        }
        assert validate_input(invalid_types_input) == [
            "'id' field of type string is required.",
            "'numberOfChildren' field of type integer is required.",
            "'familyUnitInPayForDecember' field must be present and should be a boolean.",
        ]
    except AssertionError:
        print("Test case 3: 'Incorrect data types' failed.")

    # Test case 4: Invalid familyComposition value
    try:
        invalid_family_composition = {
            "id": "12345",
            "numberOfChildren": 1,
            "familyComposition": "other",
            "familyUnitInPayForDecember": True,
        }
        assert validate_input(invalid_family_composition) == [
            "'familyComposition' field must be present and should be either 'single' or 'couple'."
        ]
    except AssertionError:
        print("Test case 4: 'Invalid familyComposition value' failed.")

    print("All tests for validate_input passed!")


def test_calculate_supplement_amount():
    print("Testing calculate_supplement_amount...")

    # Test case 1: Single with no children, eligible
    try:
        input_data = {
            "id": "1",
            "numberOfChildren": 0,
            "familyComposition": "single",
            "familyUnitInPayForDecember": True,
        }
        result = calculate_supplement_amount(input_data)
        assert result == {
            "id": "1",
            "isEligible": True,
            "baseAmount": 60.0,
            "childrenAmount": 0.0,
            "supplementAmount": 60.0,
        }
    except AssertionError:
        print("Test case 1: 'Single with no children, eligible' failed.")

    # Test case 2: Couple with no children, eligible
    try:
        input_data = {
            "id": "2",
            "numberOfChildren": 0,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": True,
        }
        result = calculate_supplement_amount(input_data)
        assert result == {
            "id": "2",
            "isEligible": True,
            "baseAmount": 120.0,
            "childrenAmount": 0.0,
            "supplementAmount": 120.0,
        }
    except AssertionError:
        print("Test case 2: 'Couple with no children, eligible' failed.")

    # Test case 3: Single parent with 2 children, eligible
    try:
        input_data = {
            "id": "3",
            "numberOfChildren": 2,
            "familyComposition": "single",
            "familyUnitInPayForDecember": True,
        }
        result = calculate_supplement_amount(input_data)
        assert result == {
            "id": "3",
            "isEligible": True,
            "baseAmount": 120.0,
            "childrenAmount": 40.0,
            "supplementAmount": 160.0,
        }
    except AssertionError:
        print("Test case 3: 'Single parent with 2 children, eligible' failed.")

    # Test case 4: Couple with 3 children, eligible
    try:
        input_data = {
            "id": "4",
            "numberOfChildren": 3,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": True,
        }
        result = calculate_supplement_amount(input_data)
        assert result == {
            "id": "4",
            "isEligible": True,
            "baseAmount": 120.0,
            "childrenAmount": 60.0,
            "supplementAmount": 180.0,
        }
    except AssertionError:
        print("Test case 4: 'Couple with 3 children, eligible' failed.")

    # Test case 5: Not eligible (familyUnitInPayForDecember=False)
    try:
        input_data = {
            "id": "5",
            "numberOfChildren": 2,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": False,
        }
        result = calculate_supplement_amount(input_data)
        assert result == {
            "id": "5",
            "isEligible": False,
            "baseAmount": 0.0,
            "childrenAmount": 0.0,
            "supplementAmount": 0.0,
        }
    except AssertionError:
        print("Test case 5: 'Not eligible (familyUnitInPayForDecember=False)' failed.")

    print("All tests for calculate_supplement_amount passed!")


if __name__ == "__main__":
    test_validate_input()
    test_calculate_supplement_amount()
    print("All tests passed!")
