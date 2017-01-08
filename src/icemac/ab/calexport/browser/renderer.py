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
    render_event_adapter_name = 'export-event'

    def get_add_event_for_day_url(self):
        """There are no add links needed in the export."""
        return None


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
        return 'special' if self.is_special else None

    @property
    def is_special(self):
        return self._get_field_value('special_field', default=False)

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


class ForecastExportList(icemac.ab.calendar.browser.renderer.base.Calendar):
    """Render events as forecast list."""

    grok.name('export-forecast-list')

    def render(self):
        rendered = []
        for ev in self.events:
            view = zope.component.getMultiAdapter(
                (ev, self.request), name='export-forecast-event')
            rendered_event = view()
            if rendered_event:
                rendered.append(rendered_event)
        if rendered:
            rendered.insert(0, '<dl>')
            rendered.append('</dl>')
        return '\n'.join(rendered)


class ExportForecastEvent(ExportEvent):
    """Export an event in the forecast list."""

    def __call__(self):
        if self.is_special:
            return super(ExportForecastEvent, self).__call__()
        return ''

    def date(self):
        formatter = self.request.locale.dates.getFormatter(
            'date', 'short')
        return formatter.format(self.context.datetime)

    def datetime(self):
        return "{date} {time}".format(date=self.date(), time=self.time())
