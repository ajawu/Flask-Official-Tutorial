from .auth import bp, register, login, logout, change_password

bp.add_url_rule('/register', view_func=register, methods=('GET', 'POST',))
bp.add_url_rule('/login', view_func=login, methods=('GET', 'POST',))
bp.add_url_rule('/logout', view_func=logout, methods=('GET',))
bp.add_url_rule('/change-password', view_func=change_password, methods=('GET', 'POST',))
