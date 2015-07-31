from mock import patch
import icemac.ab.calexport.testing


class ExportEventDdClassTests(icemac.ab.calexport.testing.ZODBTestCase):
    """Testing ..renderer.ExportEvent.dd_class()"""

    def setUp(self):
        super(ExportEventDdClassTests, self).setUp()
        calendar = self.layer['addressbook'].calendar
        self.create_special_field(
            icemac.ab.calexport.interfaces.IExportMasterdata(calendar))

    def callMUT(self, event):
        from icemac.ab.calendar.browser.renderer.interfaces import (
            IEventDescription)
        from ..renderer import ExportEvent
        get_time_zone_name = (
            'icemac.addressbook.preferences.utils.get_time_zone_name')
        with patch(get_time_zone_name, return_value='UTC'):
            context = IEventDescription(event)
        view = ExportEvent()
        view.context = context
        return view.dd_class()

    def getRecurredEvent(self, with_special_field, special_field_value=None):
        from icemac.ab.calendar.interfaces import IRecurringEvent
        event_start = self.get_datetime((2015, 7, 30, 20))
        data = {'datetime': event_start,
                'category': self.create_category(u'cat')}
        if with_special_field:
            recurring_special_field = self.create_special_field(
                iface=IRecurringEvent, set_on_masterdata=False, md=None)
            data[recurring_special_field.__name__] = special_field_value

        event = self.create_recurring_event(**data)
        return event.get_events(
            event_start, self.get_datetime((2015, 7, 31, 0))).next()

    def test_ExportEvent_dd_class_1(self):
        """ExportEvent.dd_class() can return "special" for recurred events.

        Condition: the `special_field` equivalent on the recurring event has
                   a value of `True`.
        """
        revent = self.getRecurredEvent(
            with_special_field=True, special_field_value=True)
        self.assertEqual('special', self.callMUT(revent))

    def test_ExportEvent_dd_class_2(self):
        """ExportEvent.dd_class() can return `None` for recurred events.

        Condition: the `special_field` equivalent on the recurring event has
                   a false like value.
        """
        revent = self.getRecurredEvent(
            with_special_field=True, special_field_value=None)
        self.assertIsNone(self.callMUT(revent))

    def test_ExportEvent_dd_class_3(self):
        """ExportEvent.dd_class() can return `None` for recurred events.

        Condition: there is no `special_field` equivalent on the recurring
                   event.
        """
        revent = self.getRecurredEvent(with_special_field=False)
        self.assertIsNone(self.callMUT(revent))
