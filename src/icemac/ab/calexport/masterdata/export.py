from icemac.addressbook.i18n import _
import gocept.reference
import grokcore.annotation as grok
import icemac.ab.calendar.interfaces
import icemac.ab.calendar.masterdata.calendar
import icemac.ab.calexport.interfaces
import icemac.addressbook.browser.base
import icemac.addressbook.browser.metadata
import icemac.addressbook.fieldsource
import icemac.addressbook.interfaces
import zope.schema.fieldproperty


class Masterdata(icemac.addressbook.browser.base.GroupEditForm):
    """Edit the calendar export settings."""

    label = _(u'Configure the calendar html export')
    groups = (icemac.ab.calendar.masterdata.calendar.ModifierMetadataGroup,)
    interface = icemac.ab.calexport.interfaces.IExportMasterdata
    next_url = 'parent'


class ExportMasterData(grok.Annotation):
    """Store export master data in annotations."""

    schema = icemac.ab.calexport.interfaces.IExportMasterdata
    grok.context(icemac.ab.calendar.interfaces.ICalendar)
    grok.implements(schema,
                    zope.annotation.interfaces.IAttributeAnnotatable)
    grok.provides(schema)

    zope.schema.fieldproperty.createFieldProperties(
        schema, omit=['categories', 'special_field', 'url_field'])

    categories = gocept.reference.ReferenceCollection(
        'categories', ensure_integrity=True)
    _special_field = None
    _url_field = None

    def __init__(self, *args, **kw):
        super(ExportMasterData, self).__init__(*args, **kw)
        self.categories = set([])

    @property
    def special_field(self):
        return self._field_getter('_special_field')

    @special_field.setter
    def special_field(self, value):
        self._field_setter('_special_field', value)

    @property
    def url_field(self):
        return self._field_getter('_url_field')

    @url_field.setter
    def url_field(self, value):
        self._field_setter('_url_field', value)

    def _field_getter(self, name):
        value = getattr(self, name)
        if value is None:
            return None
        try:
            return icemac.addressbook.fieldsource.untokenize(value)[1]
        except KeyError:
            return None

    def _field_setter(self, name, value):
        if value is None:
            setattr(self, name, None)
        else:
            event_entity = icemac.addressbook.interfaces.IEntity(
                icemac.ab.calendar.interfaces.IEvent)
            setattr(self, name, icemac.addressbook.fieldsource.tokenize(
                event_entity, value.__name__))
