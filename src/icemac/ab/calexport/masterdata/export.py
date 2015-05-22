import icemac.ab.calexport.interfaces
import icemac.addressbook.browser.base


class Masterdata(icemac.addressbook.browser.base.GroupEditForm):
    """Edit the calendar export settings."""

    interface = icemac.ab.calexport.interfaces.IExportMasterdata
    next_url = 'parent'
