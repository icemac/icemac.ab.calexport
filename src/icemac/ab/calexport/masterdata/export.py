import icemac.ab.calexport.interfaces
import icemac.addressbook.browser.base


class Masterdata(icemac.addressbook.browser.base.GroupEditForm):
    """Edit the calendar export settings."""

    interface = icemac.ab.calexport.interfaces.IExportMasterdata
    next_url = 'parent'


# class AnnotationField(icemac.addressbook.browser.datamanager.AnnotationField,
#                       grok.MultiAdapter):

#     """Special AnnotationField for calendar."""

#     grok.adapts(icemac.ab.calendar.interfaces.ICalendar,
#                 zope.schema.interfaces.IField)

#     no_security_proxy = (
#         icemac.ab.calendar.interfaces.ICalendarDisplaySettings,)
