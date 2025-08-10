import os
import pickle
from datetime import datetime
from flask import Blueprint, redirect, request, session as flask_session, url_for, jsonify
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint("calendar", __name__, url_prefix="/calendar")
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS_PATH = os.path.join("src", "instance", "credentials.json")
TOKEN_DIR = os.path.join("src", "instance")  # Store token_*.pkl here

def get_token_path(user_id):
    return os.path.join(TOKEN_DIR, f"token_{user_id}.pkl")

@bp.route("/authorize")
@jwt_required()
def authorize():
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        redirect_uri=url_for("calendar.callback", _external=True)
    )
    auth_url, _ = flow.authorization_url(prompt='consent')
    flask_session["flow_state"] = flow.state
    flask_session["user_id"] = get_jwt_identity()  # Store user_id for callback
    return redirect(auth_url)

@bp.route("/callback")
def callback():
    user_id = flask_session.get("user_id")
    if not user_id:
        return jsonify({"msg": "Missing user context"}), 400

    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        state=flask_session.get("flow_state"),
        redirect_uri=url_for("calendar.callback", _external=True)
    )
    flow.fetch_token(authorization_response=request.url)

    # Save credentials
    token_path = get_token_path(user_id)
    with open(token_path, "wb") as token:
        pickle.dump(flow.credentials, token)

    return redirect("/dashboard")  # Or some configurable frontend redirect

import os
import pickle
from datetime import datetime
from flask import Blueprint, redirect, request, session as flask_session, url_for, jsonify
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint("calendar", __name__, url_prefix="/calendar")

# 🔒 Scopes & credential paths
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS_PATH = os.path.join("src", "instance", "credentials.json")
TOKEN_DIR = os.path.join("src", "instance")

def get_token_path(user_id):
    return os.path.join(TOKEN_DIR, f"token_{user_id}.pkl")

# 🔐 Step 1: Begin authorization flow
@bp.route("/authorize")
@jwt_required()
def authorize():
    user_id = get_jwt_identity()

    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        redirect_uri=url_for("calendar.callback", _external=True)
    )
    auth_url, _ = flow.authorization_url(prompt='consent')

    flask_session["flow_state"] = flow.state
    flask_session["user_id"] = user_id

    return redirect(auth_url)

# 🔐 Step 2: Handle Google callback and store credentials
@bp.route("/callback")
def callback():
    user_id = flask_session.get("user_id")
    state = flask_session.get("flow_state")

    if not user_id or not state:
        return jsonify({"msg": "Missing session context"}), 400

    try:
        flow = Flow.from_client_secrets_file(
            CREDENTIALS_PATH,
            scopes=SCOPES,
            state=state,
            redirect_uri=url_for("calendar.callback", _external=True)
        )
        flow.fetch_token(authorization_response=request.url)

        token_path = get_token_path(user_id)
        with open(token_path, "wb") as token_file:
            pickle.dump(flow.credentials, token_file)

        return redirect("/dashboard")  # Or configurable frontend redirect

    except Exception as e:
        return jsonify({"msg": f"Authorization failed: {e}"}), 500

# 📅 Step 3: Fetch upcoming events
@bp.route("/events")
@jwt_required()
def get_events():
    user_id = get_jwt_identity()
    token_path = get_token_path(user_id)

    if not os.path.exists(token_path):
        return jsonify({"msg": "Google Calendar not linked"}), 403

    try:
        with open(token_path, "rb") as token_file:
            creds = pickle.load(token_file)

        service = build("calendar", "v3", credentials=creds)
        events_result = service.events().list(
            calendarId="primary",
            timeMin=datetime.utcnow().isoformat() + "Z",
            maxResults=10,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        return jsonify(events_result.get("items", []))

    except Exception as e:
        return jsonify({"msg": f"Failed to fetch events: {e}"}), 500