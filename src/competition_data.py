from datetime import datetime


class CompetitionData:
    """Represents a competition, storing the data of the events."""

    def __init__(self, name: str, events_data: dict, events_params: dict = {}, start_date: datetime = None, entry_list: dict = None):
        """
        Parameters
        ----------
        name : str
            The name of the competition
        events_data : dict
            A dictionary that stores for each event its data. Example:
            {
                'event_name_1' : {
                    'name' : "Event 1 name",
                    'sex' : ['male', 'female', 'mixed'],
                    'maximize' : False,
                    'in_group' : False,
                },
                ...
            }
        events_params : dict, optional
            A dictionary that stores for each event and gender some parameters values. Example:
            {
                'event_name_1' : {
                    'male' : {
                        'param-name-1' : 'param-value-1',
                        'param-name-2' : 'param-value-2',
                        ...
                    },
                    ...
                },
                ...
            }
        start_date : datetime, optional
            Date when the competition starts
        entry_list : dict, optional
            A dictionary that stores for each event and gender a list of the athletes names 
            that will participate in the competition. Example:
            {
                'event_name_1' : {
                    'male' : [
                        'athlete-name-1',
                        'athlete-name-2',
                        ...
                    ],
                    ...
                },
                ...
            }
        """
        
        self._events_data = events_data
        self._events_params = events_params
        self._entry_list = entry_list
        self.events = [n for n in events_data.keys()]
        self.name = name
        self.start_date = start_date

    def _check_valid_event(self, event: str) -> None:
        if event not in self.events:
            raise Exception(f"The event {event} is not registered in the competition.")

    def is_maximize_event(self, event: str) -> bool:
        """Returns true if the goal of an event is to maximize the result."""

        self._check_valid_event(event)
        return self._events_data[event]['maximize']

    def is_event_in_group(self, event: str) -> bool:
        """Returns true if the event is in groups category."""

        self._check_valid_event(event)
        return self._events_data[event]['in_group']  

    def is_in_entry_list(self, event: str, sex: str, athlete: str) -> bool:
        """Returns true if the athlete is in the entry list of the competition."""

        self._check_valid_event(event)
        return (self._entry_list is None) or (athlete.casefold() in self._entry_list[event][sex])

    def get_event_data(self, event: str, param: str):
        """Returns the data of an event."""
        
        self._check_valid_event(event)
        return self._events_data[event][param]

    def get_event_param(self, event: str, sex: str, param: str, default=None):
        """Returns the value of a specific parameter for an event."""

        self._check_valid_event(event)

        if event not in self._events_params:
            return default

        event_sex = self._events_params[event]
        if sex not in event_sex:
            return default    

        return event_sex[sex].get(param, default)

    def set_event_param(self, event: str, sex: str, param: str, value) -> None:
        """Updates the value of the parameter in the event."""
        
        self._check_valid_event(event)

        if event not in self._events_params:
            self._events_params[event] = {}
        if sex not in self._events_params[event]:
            self._events_params[event][sex] = {}
        self._events_params[event][sex][param] = value


__all__ = [
    "CompetitionData",
]