import gocept.reference.field
from icemac.addressbook.i18n import _
import icemac.ab.calendar.interfaces
import zope.interface
import zope.schema


PACKAGE_ID = 'icemac.ab.calexport'


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

    categories = gocept.reference.field.Set(
        title=_('Export only events having one of these categories'),
        required=False,
        value_type=zope.schema.Choice(
            title=_('event category'),
            source=icemac.ab.calendar.interfaces.category_source))
