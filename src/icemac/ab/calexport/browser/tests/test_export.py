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

    def get_masterdata(self):
        from icemac.ab.calexport.interfaces import IExportMasterdata
        return IExportMasterdata(self.layer['addressbook'].calendar)

    def test_returns_head_calendar_and_foot(self):
        md = self.get_masterdata()
        md.html_head = u'<html-head>'
        md.html_foot = u'</html-foot>'
        browser = self.get_browser('cal-exporter')
        browser.open('http://localhost/ab/++attribute++calendar')
        browser.getControl('Export current month').click()
        self.assertEqual(
            'http://localhost/ab/++attribute++calendar/@@export-month',
            browser.url)
        self.assertStartsWith('<html-head>', browser.contents)
        self.assertIn('calendar-export-test', browser.contents)
        self.assertEndsWith('</html-foot>', browser.contents)

    def test_returns_only_events_with_selected_categories(self):
        category = self.create_category(u'selected-category-name')
        self.get_masterdata().categories = set([category])
        self.create_event(category=category, datetime=self.get_datetime())
        browser = self.get_browser('cal-exporter')
        browser.open(
            'http://localhost/ab/++attribute++calendar/@@export-month')
        self.assertIn('selected-category-name', browser.contents)
        self.assertNotIn('calendar-export-test', browser.contents)
