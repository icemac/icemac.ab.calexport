from ..renderer import ExportEvent
from icemac.ab.calendar.browser.renderer.interfaces import IEventDescription
from icemac.ab.calendar.interfaces import IRecurringEvent
import pytest


@pytest.fixture('session')
def RecurredEventFactory(
        DateTime, CategoryFactory, SpecialFieldFactory, RecurringEventFactory):
    """Create a recurred event."""
    def get_recurred_event(
            address_book, with_special_field, special_field_value=None):
        SpecialFieldFactory(address_book)  # special field on IEvent
        event_start = DateTime(2015, 7, 30, 20)
        data = {'datetime': event_start,
                'period': 'weekly',
                'category': CategoryFactory(address_book, u'cat')}
        if with_special_field:
            recurring_special_field = SpecialFieldFactory(
                address_book, IRecurringEvent)
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


# class ExportEventDdClassTests(icemac.ab.calexport.testing.ZODBTestCase):
#     """Testing ..renderer.ExportEvent.dd_class()"""

#     def setUp():
#         super(ExportEventDdClassTests, self).setUp()
#         calendar = self.layer['addressbook'].calendar
#         self.create_special_field(
#             icemac.ab.calexport.interfaces.IExportMasterdata(calendar))

#     def callMUT(self, event):
#         from icemac.ab.calendar.browser.renderer.interfaces import (
#             IEventDescription)
#         from ..renderer import ExportEvent
#         get_time_zone_name = (
#             'icemac.addressbook.preferences.utils.get_time_zone_name')
#         with patch(get_time_zone_name, return_value='UTC'):
#             context = IEventDescription(event)
#         view = ExportEvent()
#         view.context = context
#         return view.dd_class()

#     def getRecurredEvent(self, with_special_field, special_field_value=None):
#         from icemac.ab.calendar.interfaces import IRecurringEvent
#         event_start = self.get_datetime((2015, 7, 30, 20))
#         data = {'datetime': event_start,
#                 'period': 'weekly',
#                 'category': self.create_category(u'cat')}
#         if with_special_field:
#             recurring_special_field = self.create_special_field(
#                 iface=IRecurringEvent, set_on_masterdata=False, md=None)
#             data[recurring_special_field.__name__] = special_field_value

#         event = self.create_recurring_event(**data)
#         return event.get_events(
#             event_start, self.get_datetime((2015, 7, 31, 0))).next()

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
