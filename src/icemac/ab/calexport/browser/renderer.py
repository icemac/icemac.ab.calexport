import grokcore.component as grok
import icemac.ab.calendar.browser.renderer.table
import icemac.ab.calendar.interfaces
import icemac.ab.calexport.interfaces
import icemac.addressbook.entities
import zope.cachedescriptors.property
import zope.security.proxy


class ExportTable(icemac.ab.calendar.browser.renderer.table.Table):
    """Tabular export of a calendar."""

    grok.name('export-table')
    may_render_days_as_add_links = False
    render_event_adapter_name = 'export-event'


class ExportEvent(icemac.ab.calendar.browser.renderer.table.TableEvent):
    """Export the data of an event in a table."""

    default_text = u''  # Do not render events without title

    @property
    def masterdata(self):
        # Without the following line we get a ForbiddenError for `__getitem__`
        # when accessing the annotations where `IExportMasterdata` are stored.
        # As only authorized users are able to access this function, this is no
        # security hole.
        unsave_calendar = zope.security.proxy.getObject(
            icemac.ab.calendar.interfaces.ICalendar(self.context))
        return icemac.ab.calexport.interfaces.IExportMasterdata(
            unsave_calendar)

    def action_url(self):
        return self._get_field_value('url_field', default=None)

    def info(self):
        return []

    def dd_class(self):
        is_special = self._get_field_value('special_field', default=False)
        return 'special' if is_special else None

    def _get_field_value(self, name, default):
        field = getattr(self.masterdata, name)
        if not field:
            return default
        event = icemac.ab.calendar.interfaces.IEvent(self.context)
        field = icemac.addressbook.entities.get_bound_schema_field(
            event, None, field, default_attrib_fallback=False)
        try:
            value = field.get(field.context)
        except AttributeError:  # Recurring event has no matching field:
            value = default
        return value
