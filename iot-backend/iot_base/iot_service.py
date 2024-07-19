from datetime import datetime

from .model import IOTEventRepo, IOTEvent


class IOTEventService:

    def __init__(self, iot_event_repo: IOTEventRepo):
        self.iot_event_repo = iot_event_repo

    def create_iot_event(self, iot_event_request):
        """
        Creates an IoT event based on the provided request and stores it in the repository.
        """
        iot_event_model = self.__assemble_iot_event_model(iot_event_request)
        return self.iot_event_repo.create_iot_event(iot_event_model)

    def get_events_by_device(self, iot_event_request):
        """
        Retrieves events for a specific device.

        :param iot_event_request: The request object containing device details.
        :return: A list of dictionaries containing IOTEvent details.
        """
        iot_event_records = self.iot_event_repo.get_iot_events(iot_event_request.device)
        if len(iot_event_records) < 1:
            raise ValueError("IOT device not found")
        iot_event_list = []
        for event in iot_event_records:
            iot_event_list.append(self.__prepare_iot_event_record(event))
        return iot_event_list

    def get_summary_report(self, iot_event_request):
        """
        Generates a summary report for the given device within a specified date range.

        :param iot_event_request: The request dictionaries containing device and date range details.
        :return: A list of dictionaries containing IOTEvent details with statistics.
        """
        device, start_date, end_date = iot_event_request.get("device"), iot_event_request.get(
            "start_date"), iot_event_request.get("end_date")

        # Validate input parameters
        self.__validate_device_and_dates(device, start_date, end_date)
        iot_event_records = self.iot_event_repo.get_summary_iot_events(iot_event_request)
        if len(iot_event_records) < 1:
            raise ValueError("IOT device not found")
        iot_event_list = []
        for event in iot_event_records:
            iot_event_list.append(self.__prepare_iot_event_record(event))

        return self.__calculate_statistics(iot_event_list)

    def __assemble_iot_event_model(self, iot_event_request):
        """
        Assembles an IOTEvent model from the request data.

        :param iot_event_request: The request object containing event details.
        :return: An IOTEvent model instance.
        """
        return IOTEvent(
            device=iot_event_request.device,
            event_type=iot_event_request.event_type,
            event_data=iot_event_request.event_data,
            timestamp=iot_event_request.timestamp
        )

    def __prepare_iot_event_record(self, iot_event_model):
        """
        Prepares a dictionary representation of an IOTEvent model.

        :param iot_event_model: The IOTEvent model instance.
        :return: A dictionary containing IOTEvent details.
        """
        return {
            'id': iot_event_model.id,
            'device': iot_event_model.device,
            'timestamp': iot_event_model.timestamp.strftime('%Y-%m-%d'),
            'event_type': iot_event_model.event_type,
            'event_data': iot_event_model.event_data
        }

    def __calculate_statistics(self, iot_event_list):
        """
        Calculates the min, max, and average of the event data for the list of IOT events.

        :param iot_event_list: A list of dictionaries containing IOTEvent details.
        :return: A list of dictionaries containing IOTEvent details with statistics.
        """
        event_data = []
        for event in iot_event_list:
            if 'event_data' in event:
                event_data.append(event['event_data'])
        if not event_data:
            return iot_event_list
        max_event_data = max(event_data)
        min_event_data = min(event_data)
        avg_event_data = sum(event_data) / len(event_data)

        for event in iot_event_list:
            event['max_event_data'] = max_event_data
            event['min_event_data'] = min_event_data
            event['avg_event_data'] = avg_event_data

        return iot_event_list

    def __validate_device_and_dates(self, device, start_date, end_date):
        """
        Validates the device and date range parameters.

        :param device: The device identifier.
        :param start_date: The start date as a string in 'YYYY-MM-DD' format.
        :param end_date: The end date as a string in 'YYYY-MM-DD' format.
        :raises ValueError: If any of the parameters are invalid.
        """
        if not device:
            raise ValueError("device must not be None")

        if not start_date or not end_date:
            raise ValueError("start_date and end_date must not be None")

        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("start_date and end_date must be in 'YYYY-MM-DD' format")
