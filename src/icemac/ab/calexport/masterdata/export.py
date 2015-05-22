from icemac.addressbook.i18n import _
import icemac.ab.calendar.masterdata.calendar
import icemac.ab.calexport.interfaces
import icemac.addressbook.browser.base
import icemac.addressbook.browser.metadata


class Masterdata(icemac.addressbook.browser.base.GroupEditForm):
    """Edit the calendar export settings."""

    label = _(u'Configure the calendar html export')
    groups = (icemac.ab.calendar.masterdata.calendar.ModifierMetadataGroup,)
    interface = icemac.ab.calexport.interfaces.IExportMasterdata
    next_url = 'parent'
