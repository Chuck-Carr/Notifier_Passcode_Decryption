import re
# Notifier AM2020/AFP1010/AFP200
### This takes the 7-digit hex code and converts it to the 5 digit passcode ###

print("######################################################################################")
print("This is a passcode decrypter that supports Notifier Panels AM2020 | AFP1010 | AFP200 ")
print("   You need the 7 digit Hex Code from the panel, after an invalid login attempt")
print("######################################################################################")
hex_code = input("\nEnter 7-digit Hex Code: ")

chart_1 = {
    '000': '00', '008': '01', '010': '02', '018': '03', '020': '04', '028': '05', '030': '06', '038': '07', '040': '08', '048': '09', '080': '10', '088': '11', '090': '12', '098': '13', '0A0': '14', '0A8': '15', '0B0': '16', '0B8': '17', '0C0': '18', '0C8': '19', '11D': '20', '115': '21', '10D': '22', '105': '23', '13D': '24', '135': '25', '12D': '26', '125': '27', '15D': '28', '155': '29', '19D': '30', '195': '31', '18D': '32', '185': '33', '1BD': '34', '1B5': '35', '1AD': '36', '1A5': '37', '1DD': '38', '1D5': '39', '23A': '40', '232': '41', '22A': '42', '222': '43', '21A': '44', '212': '45', '20A': '46', '202': '47', '27A': '48', '272': '49', '2BA': '50', '2B2': '51', '2AA': '52', '2A2': '53', '29A': '54', '292': '55', '28A': '56', '282': '57', '2FA': '58', '2F2': '59', '327': '60', '32F': '61', '337': '62', '33F': '63', '307': '64', '30F': '65', '317': '66', '31F': '67', '367': '68', '36F': '69', '3A7': '70', '3AF': '71', '3B7': '72', '3BF': '73', '387': '74', '38F': '75', '397': '76', '39F': '77', '3E7': '78', '3EF': '79', '474': '80', '47C': '81', '464': '82', '46C': '83', '454': '84', '45C': '85', '444': '86', '44C': '87', '434': '88', '43C': '89', '4F4': '90', '4FC': '91', '4E4': '92', '4EC': '93', '4D4': '94', '4DC': '95', '4C4': '96', '4CC': '97', '4B4': '98', '4BC': '99'
}


def closest_match(number):
    chart = [0, 8, 10, 18, 20, 28, 30, 38, 40, 48]
    closest_value = min(chart, key=lambda x: (abs(x - number), x))
    closest_index = chart.index(closest_value)
    return closest_index, closest_value


def is_hex(value):
    return bool(re.match(r'^[0-9A-Fa-f]+$', value)) and not value.isdecimal()


def convert_to_decimal(value):
    if is_hex(value):
        return int(value, 16)
    else:
        return int(value)


def subtract_hex(hex1, hex2):
    num1 = int(hex1, 16)
    num2 = int(hex2, 16)
    result = num1 - num2
    return format(result, '03X')


def decrypt(hex_code):
    # Step 1: Match first 3 hex digits with the dictionary
    first_three = hex_code[:3]
    first_two_digits = chart_1.get(first_three, None)
    if not first_two_digits:
        raise ValueError(
            f"First 3 hex digits {first_three} not found in dictionary.")

    # Step 2: Convert the next 2 hex digits to decimal and find closest match
    next_two_hex = hex_code[3:5]
    next_2_decimal = convert_to_decimal(next_two_hex)
    third_digit = str(closest_match(next_2_decimal)[0])

    # Step 3: Perform subtraction with appended value and compare with dictionary
    remaining_hex = hex_code[3:]
    # Append '00' to the decimal value
    modified_decimal = str(closest_match(next_2_decimal)[1])+"00"
    result_hex = subtract_hex(remaining_hex, modified_decimal)
    final_two_digits = chart_1.get(result_hex, None)
    if not final_two_digits:
        raise ValueError(
            f"Modified hex code {result_hex} not found in dictionary.")

    # Return the full 5-digit passcode
    passcode = first_two_digits + third_digit + final_two_digits

    return passcode


try:
    passcode = decrypt(hex_code)
    print(f"\nPasscode: {passcode}")
except ValueError as e:
    print(e)
