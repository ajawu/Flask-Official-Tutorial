from flaskr.auth import auth


auth.auth_bp.add_url_rule('/register', view_func=auth.register, methods=('GET', 'POST',))
auth.auth_bp.add_url_rule('/login', view_func=auth.login, methods=('GET', 'POST',))
auth.auth_bp.add_url_rule('/logout', view_func=auth.logout, methods=('GET',))
auth.auth_bp.add_url_rule('/change-password', view_func=auth.change_password, methods=('GET', 'POST',))
auth.auth_bp.add_url_rule('/profile', view_func=auth.profile, methods=('GET',))
auth.auth_bp.add_url_rule('/settings', view_func=auth.settings, methods=('GET',))
