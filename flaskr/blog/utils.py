def allowed_file(file_name_list: list) -> bool:
    """Return True if file extension of all passed file names is allowed"""
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    for file_name in file_name_list:
        if not file_name:
            return False
        if file_name.split('.')[-1].lower() not in allowed_extensions:
            return False
    return True


def get_category_ids(form_data: dict) -> list:
    """Extract all category ids from the form data dictionary"""
    category_ids = []
    for key in form_data:
        if key.startswith('category-'):
            category_ids.append(form_data[key])
    return category_ids
