from src.controllers.admin_controller import admin
from src.controllers.albums_controller import albums
from src.controllers.artists_controller import artists
from src.controllers.auth_controller import auth
from src.controllers.trackratings_controller import trackratings
from src.controllers.tracks_controller import tracks
from src.controllers.users_controller import users


registerable_controllers = [
    admin,
    albums,
    artists,
    auth,
    trackratings,
    tracks,
    users
]
