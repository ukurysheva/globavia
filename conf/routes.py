from flask_restful import Api
""" 
from api.handlers.UserHandlers import (
    Index,
    Register, CreateUser, LoginUser, LogoutUser, RefreshToken, InfoAcc, ChangeInfoAcc, CreatePurchase, GetPurchase
)


def generate_routes(app):
    # Create api.
    api = Api(app)

    # Add all routes resources.
    # Index page.
    api.add_resource(Index, "/")

    # Register page.
    api.add_resource(Register, "/v1/auth/register")

    # ADMIN LOGIN AND LOGOUT.
    # Login page Admin.
    # api.add_resource(Login, "/v1/auth/admin/sign-in")

    # Logout page Admin.
    # api.add_resource(Logout, "/v1/auth/admin/sign-out")

    # Refresh token.
    # api.add_resource(RefreshToken, "/v1/auth/admin/token/refresh")


    # Password reset page. Not forgot.
    # api.add_resource(ResetPassword, "/v1/auth/password_reset")

    # Example user handler for user permission.
    # api.add_resource(DataUserRequired, "/data_user")

    # Example admin handler for admin permission.
    # api.add_resource(DataAdminRequired, "/data_admin")

    # Get users page with admin permissions.
    # api.add_resource(UsersData, "/users")






    # USER LOGIN AND LOGOUT.
    # Create page User.
    #api.add_resource(CreateUser, "/v1/auth/user/sign-up")

    # Login page User.
    #api.add_resource(LoginUser, "/v1/auth/user/sign-in")

    # Logout page User.
    #api.add_resource(LogoutUser, "/v1/auth/user/sign-out")

    # Refresh token.
    #api.add_resource(RefreshToken, "/v1/auth/user/token/refresh")

    # Get Information Page.
    #api.add_resource(InfoAcc, "/v1/users")

    # Change Information Page.
    #api.add_resource(ChangeInfoAcc, "/v1/users")

    # Create Purchase.
    #api.add_resource(CreatePurchase, "/v1/users/purchases")

    # Get Purchase by id.
    #api.add_resource(GetPurchase, "/v1/users/purchases/<int: id>")

"""
