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

    form_class = None
    renderer_name = 'export-table'

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
        return '\n'.join([self.masterdata.html_head,
                          self.render_calendar(),
                          self.masterdata.html_foot])

    def get_event_descriptions(self):
        return [
            x
            for x in super(CalendarExportView, self).get_event_descriptions()
            if self.category_filter(x.context)]

    def render_calendar(self):
        """Render the calendar of the selected month."""
        headline = '<h2>{} {}</h2>\n'.format(
            self.get_month_name(self.month), self.calendar_year)
        calendar = super(CalendarExportView, self).render_calendar()
        return headline + calendar

    def category_filter(self, event):
        """Return a bool whether the event is in the categories for export."""
        return event.category in self.categories
