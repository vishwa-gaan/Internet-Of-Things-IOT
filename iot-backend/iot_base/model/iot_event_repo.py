from DataBase import DatabaseService
from .iot_event import IOTEvent


class IOTEventRepo:

    def __init__(self, database: DatabaseService):
        self.database = database
        self.dbSession = self.database.session
        pass

    def create_iot_event(self, iot_event_model):
        try:
            # Add the new event to the session
            self.dbSession.add(iot_event_model)
            # Commit the session to persist the changes
            self.dbSession.commit()
            # Refresh the instance to get the id
            self.dbSession.refresh(iot_event_model)
            return iot_event_model
        except Exception as e:
            # Rollback the session in case of any error
            self.dbSession.rollback()
            print(f"Failed to store IOT Event: {str(e)}")
        finally:
            # Close the session
            self.dbSession.close()

    def get_iot_events(self, device):
        iot_event_records = self.dbSession.query(IOTEvent).filter_by(device=device).all()
        return iot_event_records

    def get_summary_iot_events(self, iot_event_request):
        start_date = iot_event_request.get("start_date")
        end_date = iot_event_request.get("end_date")
        device = iot_event_request.get("device")

        iot_event_records = self.dbSession.query(IOTEvent).filter(
            IOTEvent.device == device,
            IOTEvent.timestamp >= start_date,
            IOTEvent.timestamp <= end_date
        ).all()
        return iot_event_records
