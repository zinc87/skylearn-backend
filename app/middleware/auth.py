from functools import wraps
from flask import request, jsonify, g
from jose import jwt, JWTError
import requests as http_requests
from app.config import Config
from app.models.user import User
from app import db

_jwks_cache = None

def _get_jwks():
    """Fetch and cache Cognito's public keys."""
    global _jwks_cache
    if _jwks_cache is None:
        url = (
            f"https://cognito-idp.{Config.COGNITO_REGION}.amazonaws.com/"
            f"{Config.COGNITO_USER_POOL_ID}/.well-known/jwks.json"
        )
        _jwks_cache = http_requests.get(url).json()["keys"]
    return _jwks_cache

def _decode_token(token: str) -> dict:
    """Decode and verify a Cognito JWT token."""
    headers = jwt.get_unverified_headers(token)
    kid = headers["kid"]
    keys = _get_jwks()
    key = next((k for k in keys if k["kid"] == kid), None)
    if not key:
        raise JWTError("Public key not found")

    return jwt.decode(
        token,
        key,
        algorithms=["RS256"],
        audience=Config.COGNITO_APP_CLIENT_ID,
        issuer=f"https://cognito-idp.{Config.COGNITO_REGION}.amazonaws.com/{Config.COGNITO_USER_POOL_ID}",
    )

def require_auth(f):
    """Decorator that protects a route — requires a valid Cognito JWT."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing authorization token"}), 401

        token = auth_header.split(" ", 1)[1]
        try:
            payload = _decode_token(token)
            g.user_id = payload["sub"]
            g.email = payload.get("email", "")
            g.username = payload.get("cognito:username", payload.get("email", "").split("@")[0])

            # Auto-create user record on first login
            user = User.query.get(g.user_id)
            if not user:
                user = User(
                    id=g.user_id,
                    username=g.username,
                    email=g.email,
                )
                db.session.add(user)
                db.session.commit()

        except (JWTError, Exception) as e:
            return jsonify({"error": f"Invalid token: {str(e)}"}), 401

        return f(*args, **kwargs)
    return decorated
