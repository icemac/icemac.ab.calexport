from icemac.addressbook.i18n import _
import gocept.reference
import grokcore.annotation as grok
import icemac.ab.calendar.interfaces
import icemac.ab.calendar.masterdata.breadcrumb
import icemac.ab.calendar.masterdata.calendar
import icemac.ab.calexport.interfaces
import icemac.addressbook.browser.base
import icemac.addressbook.browser.interfaces
import icemac.addressbook.browser.metadata
import icemac.addressbook.fieldsource
import icemac.addressbook.interfaces
import zope.schema.fieldproperty


class Masterdata(icemac.addressbook.browser.base.GroupEditForm):
    """Edit the calendar export settings."""

    groups = (icemac.ab.calendar.masterdata.calendar.ModifierMetadataGroup,)
    interface = icemac.ab.calexport.interfaces.IExportMasterdata
    next_url = 'parent'


class ExportMasterdataBreadCrumb(
        icemac.ab.calendar.masterdata.breadcrumb.CalendarMDChildBreadcrumb):
    """Breadcrumb for the export master data edit form."""

    grok.adapts(
        Masterdata,
        icemac.addressbook.browser.interfaces.IAddressBookLayer)

    title = _(u'Configure the calendar html export')
    target_url = None


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
    special_field = icemac.ab.calendar.property.AddressBookField(
        '_special_field')
    url_field = icemac.ab.calendar.property.AddressBookField('_url_field')

    def __init__(self, *args, **kw):
        super(ExportMasterData, self).__init__(*args, **kw)
        self.categories = set([])
