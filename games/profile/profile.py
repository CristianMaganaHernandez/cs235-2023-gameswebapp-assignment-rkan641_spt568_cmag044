from flask import Blueprint, render_template
from games.auth.authentication import login_required
import games.utilities.utilities as u
import games.adapters.repository as repo
from games.profile import services

profile_blueprint = Blueprint('profile_bp', __name__)


@profile_blueprint.route('/<user_name>/profile', methods=["GET", "POST"])
@login_required
def user_profile(user_name):
    user = services.get_user(repo.repo_instance, user_name)
    rated_games = user.favourite_games
    reviews = user.reviews
    current_user_name = u.get_current_user()
    currentuser = services.get_user(repo.repo_instance, current_user_name)
    wishlist = services.get_wishlist(repo.repo_instance, currentuser)
    current_user_name = u.get_current_user()
    currentuser = services.get_user(repo.repo_instance, current_user_name)
    favorite_games = services.get_favs(repo.repo_instance, currentuser)
    fav_games_length = len(favorite_games)
    wishlist_length = len(wishlist)
    return render_template(
        "profile.html",
        current_user=user_name,
        rated_games=rated_games,
        reviews=reviews,
        wishlist=wishlist,
        favorite_games=favorite_games,
        fav_games_length=fav_games_length,
        wishlist_length=wishlist_length,
        username=current_user_name
    )
    #return render_template("profile.html", current_user=user_name)
