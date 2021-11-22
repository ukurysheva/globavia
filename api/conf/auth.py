from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JsonWebToken

# JWT creation.
jwt = JsonWebToken("eyJhbGciOiJIUzI1NiIsI", expires_in=900)

# Refresh token creation.
refresh_jwt = JsonWebToken("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJle", expires_in=3600)

# Auth object creation.
auth = HTTPTokenAuth("Bearer")