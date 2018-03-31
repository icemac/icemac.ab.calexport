import icemac.ab.calexport.interfaces
import icemac.ab.calendar.interfaces
import icemac.addressbook.generations.utils


@icemac.addressbook.generations.utils.evolve_addressbooks
def evolve(addressbook):
    """Migrate ExportMasterdata storages

    ``icemac.ab.calendar.property.AddressBookField`` expects an iterable
    instead of a string.
    """
    calendar = icemac.ab.calendar.interfaces.ICalendar(addressbook)
    md = icemac.ab.calexport.interfaces.IExportMasterdata(calendar)
    if hasattr(md, '_special_field'):
        md._special_field = (md._special_field, )
    if hasattr(md, '_url_field'):
        md._url_field = (md._url_field, )
