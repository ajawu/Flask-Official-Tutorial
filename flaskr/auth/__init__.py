from flaskr.auth import auth


auth.auth_bp.add_url_rule('/register', view_func=auth.register, methods=('GET', 'POST',))
auth.auth_bp.add_url_rule('/login', view_func=auth.login, methods=('GET', 'POST',))
auth.auth_bp.add_url_rule('/logout', view_func=auth.logout, methods=('GET',))
auth.auth_bp.add_url_rule('/account-settings/', view_func=auth.account_settings, methods=('GET',))
auth.auth_bp.add_url_rule('/profile-edit/', view_func=auth.edit_profile, methods=('POST',))
auth.auth_bp.add_url_rule('/change-password', view_func=auth.edit_password, methods=('POST',))
