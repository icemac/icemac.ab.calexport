from __future__ import unicode_literals
from icemac.ab.calendar.interfaces import IEvent, IRecurringEvent
from ..interfaces import EventTypedFields


def test_interfaces__EventTypedFields__getValue__1(address_book, FieldFactory):
    """It returns all user defined fields on events of the specified type."""
    FieldFactory(address_book, IEvent, 'Bool', 'bool 1')
    FieldFactory(address_book, IRecurringEvent, 'Bool', 'bool on r-event')
    FieldFactory(address_book, IEvent, 'URI', 'uri')
    FieldFactory(address_book, IEvent, 'Bool', 'bool 2')
    source = EventTypedFields('Bool')
    assert ([u'bool 2', u'bool 1'] ==
            [x.title for x in source.factory.getValues()])
