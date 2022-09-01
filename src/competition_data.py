class CompetitionData:
    """Represents a competition, storing the data of the events."""

    def __init__(self, events_data={}, maximize_events=[], events_in_groups=[], events_params={}, entry_list=None):
        self._events_data = events_data
        self._maximize_events = maximize_events
        self._events_in_groups = events_in_groups
        self._events_params = events_params
        self._entry_list = entry_list
        self.events = [n for n in events_data.keys()]

    def get_event_data(self, event: str) -> dict:
        """Returns the data of an event."""
        
        try:
            return self._events_data[event]
        except:
            raise Exception(f"The event {event} is not registered in the competition")

    def is_maximize_event(self, event: str) -> bool:
        """Returns true if the goal of an event is to maximize the result."""

        return event in self._maximize_events

    def is_event_in_group(self, event: str) -> bool:
        """Returns true if the event is in groups category."""

        return event in self._events_in_groups  

    def get_event_param(self, event: str, sex: str, param: str, default=None):
        """Returns the value of a specific parameter for an event."""

        if event not in self._events_params:
            return default

        event_sex = self._events_params[event]
        if sex not in event_sex:
            return default    

        return event_sex[sex].get(param, default)

    def set_event_param(self, event: str, sex: str, param: str, value) -> None:
        """Updates the value of the parameter in the event."""
        
        self._events_params[event][sex][param] = value

    def is_in_entry_list(self, event: str, sex: str, athlete: str) -> bool:
        """Returns True if the athlete is in the entry list of the competition."""

        if self._entry_list is None:
            return True
        return athlete.casefold() in self._entry_list[event][sex]


__all__ = [
    "CompetitionData",
]