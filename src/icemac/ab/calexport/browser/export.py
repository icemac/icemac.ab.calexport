from icemac.addressbook.browser.base import can_access_uri_part
from icemac.addressbook.i18n import _
import grokcore.component as grok
import icemac.ab.calendar.browser.calendar
import icemac.ab.calendar.browser.interfaces
import z3c.form.button
import zope.security.proxy


def export_month(form, action):
    """Form handler function exporting the current month."""
    calendar = form.getContent().context
    form.request.response. redirect(form.url(calendar, 'export-month'))


class CalendarActions(z3c.form.button.ButtonActions,
                      grok.MultiAdapter):
    """Custom buttons actions to add the export button to the calendar form."""

    grok.adapts(
        icemac.ab.calendar.browser.calendar.MonthSelectorForm,
        icemac.ab.calendar.browser.interfaces.ICalendarLayer,
        icemac.ab.calendar.browser.calendar.MonthCalendar)

    export_button_title = _('Export current month')

    def update(self):
        can_access_export_view = can_access_uri_part(
            self.content.context, self.request, 'export-month')
        if can_access_export_view:
            export_button = z3c.form.button.Button(
                'export', title=self.export_button_title)
            self.form.buttons += z3c.form.button.Buttons(export_button)
            self.form.handlers.addHandler(
                export_button,
                z3c.form.button.Handler(export_button, export_month))
        super(CalendarActions, self).update()


class CalendarExportView(icemac.ab.calendar.browser.calendar.MonthCalendar):
    """View exporting the currently selected month as HTML."""

    renderer_name = 'export-table'

    def update_form(self):
        pass  # We do not want to render a month select form in the output.

    @zope.cachedescriptors.property.Lazy
    def masterdata(self):
        # Without the following line we get a ForbiddenError for `__getitem__`
        # when accessing the annotations where `IExportMasterdata` are stored.
        # As only authorized users are able to access this function, this is no
        # security hole.
        unsave_calendar = zope.security.proxy.getObject(self.context)
        return icemac.ab.calexport.interfaces.IExportMasterdata(
            unsave_calendar)

    @zope.cachedescriptors.property.Lazy
    def categories(self):
        return self.masterdata.categories

    def __call__(self):
        self.update()
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename={0.masterdata.filename}'.format(self))
        return '\n'.join([self.masterdata.html_head or u'',
                          self.render_calendar(),
                          self.render_forecast(),
                          self.masterdata.html_foot or u''])

    def get_event_descriptions(self):
        return [
            x
            for x in super(CalendarExportView, self).get_event_descriptions()
            if self.category_filter(x.context)]

    def render_calendar(self):
        """Render the calendar of the selected month."""
        headline = u'<h2>{} {}</h2>\n'.format(
            self.get_month_name(self.month), self.calendar_year)
        calendar = super(CalendarExportView, self).render_calendar()
        return headline + calendar

    def category_filter(self, event):
        """Return a bool whether the event is in the categories for export."""
        return event.category in self.categories

    def render_forecast(self):
        """Render special events of the 11 months after the selected month."""
        all_events = self.events_in_interval(
            self.month + 1, self.month + 11, condition=self.category_filter)
        result = ['<div>']
        result.extend(self.render_forecast_events(month, events)
                      for month, events in all_events)
        result.append('</div>')
        return '\n'.join(result)

    def render_forecast_events(self, month, events):
        headline = u'<h2>{} {}</h2>'.format(
            self.get_month_name(month), month.year)
        result = zope.component.getMultiAdapter(
            (month, self.request, events),
            icemac.ab.calendar.browser.renderer.interfaces.IRenderer,
            name='export-forecast-list')()
        if result:
            result = '\n'.join((headline, result))
        return result
