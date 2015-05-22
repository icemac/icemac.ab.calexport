import icemac.ab.calexport.testing


class CalendarActionsTests(icemac.ab.calexport.testing.BrowserTestCase):
    """Testing ..export.CalendarActions."""

    @property
    def button(self):
        from ..export import CalendarActions
        return CalendarActions.export_button_title

    def test_button_is_not_rendered_for_calendar_editor(self):
        # Because he is not allowed to export.
        browser = self.get_browser('cal-editor')
        browser.open('http://localhost/ab/++attribute++calendar')
        with self.assertRaises(LookupError):
            browser.getControl(self.button)

    def test_button_is_rendered_for_calendar_exporter(self):
        browser = self.get_browser('cal-exporter')
        browser.open('http://localhost/ab/++attribute++calendar')
        with self.assertNothingRaised():
            browser.getControl(self.button)


class CalendarExportViewTests(icemac.ab.calexport.testing.BrowserTestCase):
    """Testing ..export.CalendarExportView."""

    def setUp(self):
        super(CalendarExportViewTests, self).setUp()
        self.create_event(
            category=self.create_category(u'calendar-export-test'),
            datetime=self.get_datetime())

    def test_returns_head_calendar_and_foot(self):
        from icemac.ab.calexport.interfaces import IExportMasterdata
        md = IExportMasterdata(self.layer['addressbook'].calendar)
        md.html_head = u'<html-head>'
        md.html_foot = u'</html-foot>'
        browser = self.get_browser('cal-exporter')
        browser.open('http://localhost/ab/++attribute++calendar')
        browser.getControl('Export current month').click()
        self.assertStartsWith('<html-head>', browser.contents)
        self.assertIn('calendar-export-test', browser.contents)
        self.assertEndsWith('</html-foot>', browser.contents)
