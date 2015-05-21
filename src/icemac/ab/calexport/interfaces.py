from icemac.addressbook.i18n import _
import zope.interface
import zope.schema


PACKAGE_ID = 'icemac.ab.calexport'


class IExportMasterdata(zope.interface.Interface):
    """Masterdata for the calendar export."""

    html_header = zope.schema.Text(
        title=_('HTML header'),
        description=_('HTML text above the calendar.'),
        required=False)
