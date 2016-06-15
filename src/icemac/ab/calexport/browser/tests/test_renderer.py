from ..renderer import ExportEvent
from icemac.ab.calendar.browser.renderer.interfaces import IEventDescription
from icemac.ab.calendar.interfaces import IRecurringEvent
import pytest
import pytz


def get_recurred_event_with_custom_field(
        with_field, name, value, address_book, MasterDataFieldFactory,
        RecurringEventFactory, DateTime, CategoryFactory):
    """Get a recurred event maybe having a custom field."""
    MasterDataFieldFactory(address_book, name)  # on IEvent
    event_start = DateTime(2015, 7, 30, 20)
    data = {'datetime': event_start,
            'period': 'weekly',
            'category': CategoryFactory(address_book, u'cat')}
    if with_field:
        field = MasterDataFieldFactory(address_book, name, IRecurringEvent)
        data[field.__name__] = value

    event = RecurringEventFactory(address_book, **data)
    return event.get_events(
        event_start, DateTime(2015, 7, 31, 0), pytz.UTC).next()


@pytest.fixture('session')
def SpecialFieldRecurredEventFactory(
        DateTime, CategoryFactory, MasterDataFieldFactory,
        RecurringEventFactory):
    """Create a recurred event with a `special_field`."""
    def get_recurred_event(address_book, with_field=False, value=None):
        return get_recurred_event_with_custom_field(
            with_field, 'special_field', value, address_book,
            MasterDataFieldFactory, RecurringEventFactory, DateTime,
            CategoryFactory)
    return get_recurred_event


@pytest.fixture('session')
def URLFieldRecurredEventFactory(
        DateTime, CategoryFactory, MasterDataFieldFactory,
        RecurringEventFactory):
    """Create a recurred event with a URL field."""
    def get_recurred_event(address_book, with_field=False, value=None):
        return get_recurred_event_with_custom_field(
            with_field, 'url_field', value, address_book,
            MasterDataFieldFactory, RecurringEventFactory, DateTime,
            CategoryFactory)
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
        address_book, SpecialFieldRecurredEventFactory, ExportEventFactory):
    """It returns `"special"` for recurred events.

    Condition: the `special_field` equivalent on the recurring event has
               a value of `True`.
    """
    revent = SpecialFieldRecurredEventFactory(
        address_book, with_field=True, value=True)
    assert 'special' == ExportEventFactory(revent).dd_class()


def test_renderer__ExportEvent__dd_class__2(
        address_book, SpecialFieldRecurredEventFactory, ExportEventFactory):
    """It returns `None` for recurred events.

    Condition: the `special_field` equivalent on the recurring event has
               a false like value.
    """
    revent = SpecialFieldRecurredEventFactory(
        address_book, with_field=True, value=None)
    assert None is ExportEventFactory(revent).dd_class()


def test_renderer__ExportEvent__dd_class__3(
        address_book, SpecialFieldRecurredEventFactory, ExportEventFactory):
    """It returns `None` for recurred events.

    Condition: there is no `special_field` equivalent on the recurring
               event.
    """
    revent = SpecialFieldRecurredEventFactory(address_book, with_field=False)
    assert None is ExportEventFactory(revent).dd_class()


def test_renderer__ExportEvent__action_url__1(
        address_book, URLFieldRecurredEventFactory, ExportEventFactory):
    """It returns `None` by default."""
    revent = URLFieldRecurredEventFactory(address_book)
    assert None is ExportEventFactory(revent).action_url()


def test_renderer__ExportEvent__action_url__2(
        address_book, URLFieldRecurredEventFactory, ExportEventFactory):
    """It returns `None` by default."""
    revent = URLFieldRecurredEventFactory(
        address_book, with_field=True, value='http://event.info')
    assert 'http://event.info' is ExportEventFactory(revent).action_url()
