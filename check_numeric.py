# Define possible things
valid_province_codes = {'001', '002', '004', '006', '008', '010', '011', '012', '014', '015', 
                        '017', '019', '020', '022', '024', '025', '026', '027', '030', '031', 
                        '033', '034', '035', '036', '037', '038', '040', '042', '044', '045', 
                        '046', '048', '049', '051', '052', '054', '056', '058', '060', '062', 
                        '064', '066', '067', '068', '070', '072', '074', '075', '077', '079', 
                        '080', '082', '083', '084', '086', '087', '089', '091', '092', '093', 
                        '094', '095', '096'}
valid_gender_and_century_codes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# Function to check here
def is_valid_id_card(id_number):
    if len(id_number) != 12 or not id_number.isdigit():
        return False

    province_code = id_number[:3]
    gender_and_century_code = id_number[3:4]

    if province_code not in valid_province_codes:
        return False
    if gender_and_century_code not in valid_gender_and_century_codes:
        return False

    return True

def is_valid_passport_number(passport_number):
    if len(passport_number) > 9 or len(passport_number) < 7:
        return False
    if not passport_number[0].isalpha():
        return False
    if not passport_number[1:].isdigit():
        return False

    return True

def is_valid_phone_number(phone_number):
    if phone_number.startswith("+84"):
        phone_number = phone_number[3:]
    elif phone_number.startswith("84"):
        phone_number = phone_number[2:]

    if len(phone_number) != 10 or not phone_number.isdigit():
        return False
    
    valid_mobile_prefixes = ['03', '05', '07', '08', '09']
    valid_landline_prefixes = ['02']

    if phone_number[:2] in valid_mobile_prefixes or phone_number[:2] in valid_landline_prefixes:
        return True
    
    return False

def check_numeric(numberinput):
    if is_valid_id_card(numberinput):
        return "LABEL_3"
    elif is_valid_passport_number(numberinput):
        return "LABEL_3"
    elif is_valid_phone_number(numberinput):
        return "LABEL_3"
    elif numberinput.isdigit() and len(numberinput) > 5:
        return "LABEL_2"
    else:
        return "LABEL_1"