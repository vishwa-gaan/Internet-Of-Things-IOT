import unittest
from datetime import datetime

from iot_base import IOTEventService
from iot_base.model import IOTEventRepo, IOTEvent
from DataBase import DatabaseService


class TestIOTAPP(unittest.TestCase):

    def setUp(self):
        db_url = "postgresql://postgres:123456@localhost:5432/test_iot_db"
        self.database = DatabaseService(db_url)
        self.iot_event_repo = IOTEventRepo(self.database)
        self.iot_event_service = IOTEventService(self.iot_event_repo)

    def test_create_iot_event(self):
        request_data = {
            'device': 'test_laptop',
            'event_type': 'data_storage',
            'event_data': 25.5,
            'timestamp': datetime.now()
        }

        iot_event_request = IOTEvent(
            device=request_data.get("device"),
            timestamp=request_data.get("timestamp"),
            event_type=request_data.get("event_type"),
            event_data=request_data.get("event_data")
        )
        iot_event = self.iot_event_service.create_iot_event(iot_event_request)
        print("test_create_iot_event")
        print(iot_event.__dict__)

    def test_get_events_by_device(self):
        request_data = {'device': 'test_laptop'}

        iot_event_request = IOTEvent(device=request_data.get("device"))

        result = self.iot_event_service.get_events_by_device(iot_event_request)
        print("test_get_events_by_device")
        print(result)

    def test_get_summary_report(self):
        iot_event_request = {
            'device': 'test_laptop1',
            'start_date': '2024-07-15',
            'end_date': '2024-07-15'
        }

        result = self.iot_event_service.get_summary_report(iot_event_request)
        print("test_get_summary_report")
        print(result)


if __name__ == '__main__':
    unittest.main()
