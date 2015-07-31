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
        schema, omit=['categories', 'special_field'])

    categories = gocept.reference.ReferenceCollection(
        'categories', ensure_integrity=True)
    _special_field = None

    def __init__(self, *args, **kw):
        super(ExportMasterData, self).__init__(*args, **kw)
        self.categories = set([])

    @property
    def special_field(self):
        if self._special_field is None:
            return None
        try:
            return icemac.addressbook.fieldsource.untokenize(
                self._special_field)[1]
        except KeyError:
            return None

    @special_field.setter
    def special_field(self, field):
        if field is None:
            self._special_field = None
        else:
            event_entity = icemac.addressbook.interfaces.IEntity(
                icemac.ab.calendar.interfaces.IEvent)
            self._special_field = icemac.addressbook.fieldsource.tokenize(
                event_entity, field.__name__)
