from flask_restful import Api

from api.handlers.UserHandlers import (
    Login,
    Country,
    Countries,
    CountriesId,
    Airport,
    Airports,
    AirportsId,
    AirCompany,
    AirCompanies,
    AirCompaniesId,
    Plane,
    Planes,
    PlanesId,
    Flight,
    Flights,
    FlightsId,
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
    api.add_resource(Login, "/v1/auth/admin/sign-in")

    # Logout page Admin.
    # api.add_resource(Logout, "/v1/auth/admin/sign-out")

    # Refresh token.
    # api.add_resource(RefreshToken, "/v1/auth/admin/token/refresh")

    # COUNTRIES.
    # Create new country.
    api.add_resource(Country, "/v1/countries")

    # Get all countries.
    api.add_resource(Countries, "/v1/countries")

    # Get country by id.
    api.add_resource(CountriesId, "/v1/countries/id")


    # AIRPORTS.
    # Create new airport.
    api.add_resource(Airport, "/v1/airports")

    # Get all airports.
    api.add_resource(Airports, "/v1/airports")

    # Get airport by id.
    api.add_resource(AirportsId, "/v1/airports/id")


    # AIR COMPANY.
    # Create new air company.
    api.add_resource(AirCompany, "/v1/airlines")

    # Get all air companies.
    api.add_resource(AirCompanies, "/v1/airlines")

    # Get  air company by id.
    api.add_resource(AirCompaniesId, "/v1/airlines/id")


    # PLANE.
    # Create new plane.
    api.add_resource(Plane, "/v1/aircrafts")

    # Get all planes.
    api.add_resource(Planes, "/v1/aircrafts")

    # Get plane by id.
    api.add_resource(PlanesId, "/v1/aircrafts/id")


    # FLIGHT.
    # Create new flight.
    api.add_resource(Flight, "/v1/flights")

    # Get all flights.
    api.add_resource(Flights, "/v1/flights")

    # Get flight by id.
    api.add_resource(FlightsId, "/v1/flights/id")


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
    api.add_resource(CreateUser, "/v1/auth/user/sign-up")

    # Login page User.
    api.add_resource(LoginUser, "/v1/auth/user/sign-in")

    # Logout page User.
    api.add_resource(LogoutUser, "/v1/auth/user/sign-out")

    # Refresh token.
    api.add_resource(RefreshToken, "/v1/auth/user/token/refresh")

    # Get Information Page.
    api.add_resource(InfoAcc, "/v1/users")

    # Change Information Page.
    api.add_resource(ChangeInfoAcc, "/v1/users")

    # Create Purchase.
    api.add_resource(CreatePurchase, "/v1/users/purchases")

    # Get Purchase by id.
    api.add_resource(GetPurchase, "/v1/users/purchases/<int: id>")
