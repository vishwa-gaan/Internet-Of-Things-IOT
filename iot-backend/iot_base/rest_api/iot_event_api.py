from flask import request, jsonify, Blueprint
from datetime import datetime
from DataBase import DatabaseService
from ..iot_service import IOTEventService
from ..model import IOTEventRepo, IOTEvent

iot_blueprint = Blueprint('IOT', __name__)

# Initialize database service and repositories
data_base = DatabaseService()
iot_event_repo = IOTEventRepo(data_base)
iot_event_service = IOTEventService(iot_event_repo)


# Endpoint to welcome users
@iot_blueprint.route('/')
def index():
    return 'Welcome to IOT Event'


# Endpoint to create a new IOT event
@iot_blueprint.route('/create', methods=['POST'])
def create_event():
    request_data = request.get_json()
    iot_event_request = IOTEvent(
        device=request_data.get("device"),
        timestamp=datetime.now(),
        event_type=request_data.get("event_type"),
        event_data=request_data.get("event_data")
    )
    iot_event = iot_event_service.create_iot_event(iot_event_request)
    return jsonify({
        "id": iot_event.id,
        "device": iot_event.device,
        "event_type": iot_event.event_type,
        "event_data": iot_event.event_data,
        "timestamp": iot_event.timestamp.strftime('%Y-%m-%d')
    }), 200


# Endpoint to retrieve events for a specific device
@iot_blueprint.route('/<device>', methods=['GET'])
def get_events_by_device(device):
    iot_event_request = IOTEvent(device=device)
    iot_events = iot_event_service.get_events_by_device(iot_event_request)
    return jsonify(iot_events), 200


# Endpoint to generate a summary report for a specific device within a date range
@iot_blueprint.route('/summary/<device>', methods=['POST'])
def get_summary_report(device):
    request_data = request.get_json()
    start_date = request_data.get('start_date')
    end_date = request_data.get('end_date')

    iot_event_request = {
        'device': device,
        'start_date': start_date,
        'end_date': end_date
    }

    iot_summary = iot_event_service.get_summary_report(iot_event_request)
    return jsonify(iot_summary), 200
