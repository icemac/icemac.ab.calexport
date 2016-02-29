from icemac.addressbook.i18n import _
import gocept.reference.field
import icemac.ab.calendar.interfaces
import icemac.addressbook.interfaces
import zc.sourcefactory.basic
import zope.interface
import zope.schema


PACKAGE_ID = 'icemac.ab.calexport'


class EventBooleanFields(zc.sourcefactory.basic.BasicSourceFactory):
    """User defined boolean fields on IEvent."""

    def getValues(self):
        event_entity = icemac.addressbook.interfaces.IEntity(
            icemac.ab.calendar.interfaces.IEvent)
        for name, field in event_entity.getRawFields():
            if not icemac.addressbook.interfaces.IField.providedBy(field):
                continue
            if field.type != u'Bool':
                continue
            yield field

    def getTitle(self, value):
        return value.title

event_boolean_fields = EventBooleanFields()


class IExportMasterdata(zope.interface.Interface):
    """Masterdata for the calendar export."""

    html_head = zope.schema.Text(
        title=_('HTML to be inserted above calendar in export file'),
        default=u'',
        required=False)

    html_foot = zope.schema.Text(
        title=_('HTML to be inserted below calendar in export file'),
        default=u'',
        required=False)

    filename = zope.schema.TextLine(
        title=_('Name for the generated file when downloading'),
        default=u'export.html',
        required=True)

    categories = gocept.reference.field.Set(
        title=_('Export only events having one of these categories'),
        required=False,
        value_type=zope.schema.Choice(
            title=_('event category'),
            source=icemac.ab.calendar.interfaces.category_source))

    special_field = zope.schema.Choice(
        title=_('Use this Boolean field to determine whether the event should '
                'be rendered with the `special` CSS class'),
        source=event_boolean_fields,
        required=False)
