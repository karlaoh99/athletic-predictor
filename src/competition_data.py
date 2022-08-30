class CompetitionData:
    """Represents a competition, storing the data of the events."""

    def __init__(self, events_data={}, maximize_events=[], events_in_groups=[]):
        self._events_data = events_data
        self._maximize_events = maximize_events
        self._events_in_groups = events_in_groups
        self.events = [n for n in events_data.keys()]

    def get_event_data(self, event: str) -> dict:
        """Returns the data of an event."""
        
        try:
            return self.events_data[event]
        except:
            raise Exception(f"The event {event} is not registered in the competition")

    def is_maximize_event(self, event: str) -> bool:
        """Returns true if the goal of an event is to maximize the result."""

        return event in self._maximize_events

    def is_event_in_group(self, event: str) -> bool:
        """Returns true if the event is in groups category."""

        return event in self._events_in_groups  


__all__ = [
    "CompetitionData",
]