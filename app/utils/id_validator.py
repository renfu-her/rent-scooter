"""Taiwan ID number validator"""


def validate_taiwan_id(id_number):
    """
    Validate Taiwan ID number format and checksum
    
    Format: 1 letter (A-Z) + 1 digit (1 or 2) + 8 digits (0-9)
    Example: A123456789
    
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not id_number:
        return False, '身份證號碼不能為空'
    
    # Convert to uppercase and remove spaces
    id_number = id_number.strip().upper()
    
    # Check length
    if len(id_number) != 10:
        return False, '身份證號碼必須為10碼'
    
    # Check first character is a letter
    if not id_number[0].isalpha():
        return False, '身份證號碼第一碼必須為英文字母'
    
    # Check second character is 1 or 2
    if id_number[1] not in ('1', '2'):
        return False, '身份證號碼第二碼必須為1或2'
    
    # Check remaining characters are digits
    if not id_number[2:].isdigit():
        return False, '身份證號碼第3-10碼必須為數字'
    
    # Calculate checksum using Taiwan ID verification algorithm
    # Letter mapping: A=10, B=11, C=12, ..., Z=33
    letter_code = ord(id_number[0]) - ord('A') + 10
    
    # Split letter code into tens and ones
    # Example: A=10 -> tens=1, ones=0; B=11 -> tens=1, ones=1
    letter_tens = letter_code // 10
    letter_ones = letter_code % 10
    
    # Taiwan ID checksum formula:
    # (letter_tens×1 + letter_ones×9 + id_number[1]×8 + id_number[2]×7 + id_number[3]×6 + 
    #  id_number[4]×5 + id_number[5]×4 + id_number[6]×3 + id_number[7]×2 + id_number[8]×1) % 10 == 0
    # Note: id_number[9] is the check digit itself, not included in calculation
    # Weights array: [1, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    # Index mapping: [0:letter_tens, 1:letter_ones, 2:id_number[1], 3:id_number[2], ..., 9:id_number[8]]
    weights = [1, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    checksum = letter_tens * weights[0] + letter_ones * weights[1]
    
    # Add digits from id_number[1] to id_number[8] (8 digits, excluding check digit id_number[9])
    # weights indices 2-9 correspond to id_number indices 1-8
    for i in range(1, 9):  # i from 1 to 8 (id_number[1] to id_number[8])
        digit = int(id_number[i])
        checksum += digit * weights[i + 1]  # weights[i+1] because weights[0] and weights[1] are for letter
    
    # Add check digit (id_number[9]) with weight 1
    check_digit = int(id_number[9])
    checksum += check_digit * weights[9]  # weights[9] = 1
    
    if checksum % 10 != 0:
        return False, '身份證號碼檢查碼錯誤，請確認身份證號碼是否正確'
    
    return True, ''


def format_taiwan_id(id_number):
    """
    Format Taiwan ID number (uppercase, remove spaces)
    
    Returns:
        str: Formatted ID number
    """
    if not id_number:
        return ''
    return id_number.strip().upper()

