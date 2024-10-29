
from flask import session
from typing import Union
from games.auth.authentication import login_required


# Use if user can be logged in or not
def get_current_user() -> Union[str, None]:
    try:
        current_user = session["user_name"]
        return current_user
    except KeyError:
        return None


# Use if you are sure user is logged in
@login_required
def get_user() -> str:
    return session["user_name"]
