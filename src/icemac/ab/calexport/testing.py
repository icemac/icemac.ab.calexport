import icemac.ab.calendar.interfaces
import icemac.ab.calendar.testing
import icemac.ab.calexport
import icemac.ab.calexport.interfaces
import icemac.addressbook.testing


class Browser(icemac.ab.calendar.testing.Browser):
    """Browser adapted for calendar export."""

    CALEXPORT_MONTH_EXPORT_URL = (
        'http://localhost/ab/++attribute++calendar/@@export-month')

    CALEXPORT_MASTER_DATA_URL = (
        'http://localhost/ab/++attribute++calendar/'
        '@@edit-export-masterdata.html')


def get_masterdata(address_book):
    """Get the object providing export master data."""
    return icemac.ab.calexport.interfaces.IExportMasterdata(
        address_book.calendar)
