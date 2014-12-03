from flask.ext.login import login_user, logout_user
from flask import redirect, current_app, request

from .models import User


ID_SITE_STATUS_AUTHENTICATED = 'AUTHENTICATED'
ID_SITE_STATUS_LOGOUT = 'LOGOUT'
ID_SITE_STATUS_REGISTERED = 'REGISTERED'


def _handle_authenticated(id_site_response):
    login_user(User.from_id_site(id_site_response.account),
            remember=True)
    return redirect(request.args.get('next') or current_app.config['STORMPATH_REDIRECT_URL'])


def _handle_logout(id_site_response):
    logout_user()
    return redirect('/')


_handle_registered = _handle_authenticated


def handle_id_site_callback(id_site_response):
    if id_site_response:
        action = CALLBACK_ACTIONS[id_site_response.status]
        return action(id_site_response)
    else:
        return None


CALLBACK_ACTIONS = {
        ID_SITE_STATUS_AUTHENTICATED: _handle_authenticated,
        ID_SITE_STATUS_LOGOUT: _handle_logout,
        ID_SITE_STATUS_REGISTERED: _handle_registered
}

