def validate_required_fields(data, required_fields):
    """
    Validate that required fields are present in data
    
    Args:
        data: Dictionary to validate
        required_fields: List of required field names
    
    Returns:
        Tuple (is_valid, missing_fields)
    """
    missing_fields = [field for field in required_fields if not data.get(field)]
    return (len(missing_fields) == 0, missing_fields)

