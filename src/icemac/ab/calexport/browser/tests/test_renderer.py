from ..renderer import ExportEvent, ForecastExportList
from icemac.ab.calendar.browser.interfaces import IEventDescription
from icemac.ab.calendar.interfaces import IRecurringEvent
import pytest
import pytz


def get_recurred_event_with_custom_field(
        with_field, name, value, address_book, MasterDataFieldFactory,
        RecurringEventFactory, DateTime, CategoryFactory, category):
    """Get a recurred event maybe having a custom field."""
    MasterDataFieldFactory(address_book, name)  # on IEvent
    event_start = DateTime(2015, 7, 30, 20)
    data = {'datetime': event_start,
            'period': 'weekly',
            'category': CategoryFactory(address_book, category)}
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
    def get_recurred_event(
            address_book, with_field=False, value=None, category=u'cat'):
        return get_recurred_event_with_custom_field(
            with_field, 'special_field', value, address_book,
            MasterDataFieldFactory, RecurringEventFactory, DateTime,
            CategoryFactory, category)
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
            CategoryFactory, category=u'cat')
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


def test_renderer__ForecastExportList__render__1(
        address_book, RequestFactory, DateTime, RecurringEventFactory,
        MasterDataFieldFactory, CategoryFactory, utc_time_zone_pref):
    """It renders only events which are marked as `special`."""
    MasterDataFieldFactory(address_book, 'special_field')  # on IEvent
    field = MasterDataFieldFactory(
        address_book, 'special_field', IRecurringEvent)
    event_start = DateTime(2015, 7, 30, 20)

    # special event
    data = {'datetime': event_start,
            'period': 'weekly',
            'category': CategoryFactory(address_book, u'special-event'),
            field.__name__: True}
    special_recurring_event = RecurringEventFactory(address_book, **data)
    special_recurred_event = special_recurring_event.get_events(
        event_start, DateTime(2015, 7, 31, 0), pytz.UTC).next()

    # non special event
    data2 = {'datetime': event_start,
             'period': 'weekly',
             'category': CategoryFactory(address_book, u'normal-event'),
             field.__name__: False}
    non_special_recurring_event = RecurringEventFactory(address_book, **data2)
    non_special_recurred_event = non_special_recurring_event.get_events(
        event_start, DateTime(2015, 7, 31, 0), pytz.UTC).next()

    # forecast list
    forecast = ForecastExportList(
        month=None, request=RequestFactory(),
        events=[IEventDescription(non_special_recurred_event),
                IEventDescription(special_recurred_event)])
    assert '''\
<dl>
<dt>15/07/30 20:00</dt>
<dd>special-event</dd>

</dl>''' == forecast.render()


def test_renderer__ForecastExportList__render__2(
        address_book, RequestFactory, DateTime, RecurringEventFactory,
        MasterDataFieldFactory, CategoryFactory, utc_time_zone_pref):
    """It localizes the time to the locale of the user."""
    MasterDataFieldFactory(address_book, 'special_field')  # on IEvent
    field = MasterDataFieldFactory(
        address_book, 'special_field', IRecurringEvent)
    event_start = DateTime(2015, 7, 30, 20)

    # special event
    data = {'datetime': event_start,
            'period': 'weekly',
            'category': CategoryFactory(address_book, u'Frauentreffen'),
            field.__name__: True}
    special_recurring_event = RecurringEventFactory(address_book, **data)
    special_recurred_event = special_recurring_event.get_events(
        event_start, DateTime(2015, 7, 31, 0), pytz.UTC).next()

    # forecast list
    forecast = ForecastExportList(
        month=None, request=RequestFactory(HTTP_ACCEPT_LANGUAGE='de_DE'),
        events=[IEventDescription(special_recurred_event)])
    assert '''\
<dl>
<dt>30.07.15 20:00 Uhr</dt>
<dd>Frau&shy;en&shy;tref&shy;fen</dd>

</dl>''' == forecast.render()
