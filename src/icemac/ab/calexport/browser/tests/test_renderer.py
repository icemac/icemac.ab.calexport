from ..renderer import ExportEvent
from icemac.ab.calendar.browser.renderer.interfaces import IEventDescription
from icemac.ab.calendar.interfaces import IRecurringEvent
import pytest


@pytest.fixture('session')
def RecurredEventFactory(
        DateTime, CategoryFactory, MasterDataFieldFactory,
        RecurringEventFactory):
    """Create a recurred event."""
    def get_recurred_event(
            address_book, with_special_field, special_field_value=None):
        MasterDataFieldFactory(address_book, 'special_field')  # on IEvent
        event_start = DateTime(2015, 7, 30, 20)
        data = {'datetime': event_start,
                'period': 'weekly',
                'category': CategoryFactory(address_book, u'cat')}
        if with_special_field:
            recurring_special_field = MasterDataFieldFactory(
                address_book, 'special_field', IRecurringEvent)
            data[recurring_special_field.__name__] = special_field_value

        event = RecurringEventFactory(address_book, **data)
        return event.get_events(event_start, DateTime(2015, 7, 31, 0)).next()
    return get_recurred_event


@pytest.fixture('function')
def ExportEventFactory(utc_time_zone_pref):
    """Create the `ExportEvent` view for an event."""
    def get_export_event(event):
        view = ExportEvent()
        view.context = IEventDescription(event)
        return view
    return get_export_event


def test_renderer__ExportEvent__dd_class__1(
        address_book, RecurredEventFactory, ExportEventFactory):
    """It returns `"special"` for recurred events.

    Condition: the `special_field` equivalent on the recurring event has
               a value of `True`.
    """
    revent = RecurredEventFactory(
        address_book, with_special_field=True, special_field_value=True)
    assert 'special' == ExportEventFactory(revent).dd_class()


def test_renderer__ExportEvent__dd_class__2(
        address_book, RecurredEventFactory, ExportEventFactory):
    """It returns `None` for recurred events.

    Condition: the `special_field` equivalent on the recurring event has
               a false like value.
    """
    revent = RecurredEventFactory(
        address_book, with_special_field=True, special_field_value=None)
    assert None is ExportEventFactory(revent).dd_class()


def test_renderer__ExportEvent__dd_class__3(
        address_book, RecurredEventFactory, ExportEventFactory):
    """It returns `None` for recurred events.

    Condition: there is no `special_field` equivalent on the recurring
               event.
    """
    revent = RecurredEventFactory(address_book, with_special_field=False)
    assert None is ExportEventFactory(revent).dd_class()
