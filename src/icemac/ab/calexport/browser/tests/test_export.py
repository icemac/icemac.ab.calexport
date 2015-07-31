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
        self.ab = self.layer['addressbook']
        self.category = self.create_category(u'calendar-export-test')
        self.create_event(
            category=self.category, datetime=self.get_datetime())
        self.get_masterdata().categories = set([self.category])

    def get_masterdata(self):
        from icemac.ab.calexport.interfaces import IExportMasterdata
        return IExportMasterdata(self.layer['addressbook'].calendar)

    def test_returns_no_events_if_no_categories_set(self):
        self.get_masterdata().categories = set()
        browser = self.get_browser('cal-exporter')
        browser.open('http://localhost/ab/++attribute++calendar')
        browser.getControl('Export current month').click()
        self.assertEqual(
            'http://localhost/ab/++attribute++calendar/@@export-month',
            browser.url)
        self.assertNotIn('<dd>', browser.contents)

    def test_returns_head_calendar_and_foot(self):
        md = self.get_masterdata()
        md.categories = set([self.category])
        md.html_head = u'<html-head>'
        md.html_foot = u'</html-foot>'
        browser = self.get_browser('cal-exporter')
        browser.open(
            'http://localhost/ab/++attribute++calendar/@@export-month')
        self.assertStartsWith('<html-head>', browser.contents)
        self.assertEllipsis(
            '...<dd> calendar-export-test </dd>...', browser.contents)
        self.assertEndsWith('</html-foot>', browser.contents)

    def test_returns_only_events_with_selected_categories(self):
        category = self.create_category(u'selected-category-name')
        self.get_masterdata().categories = set([category])
        self.create_event(category=category, datetime=self.get_datetime())
        browser = self.get_browser('cal-exporter')
        browser.open(
            'http://localhost/ab/++attribute++calendar/@@export-month')
        self.assertEllipsis(
            '...<dd> selected-category-name </dd>...', browser.contents)
        self.assertNotIn('calendar-export-test', browser.contents)

    def test_sets_special_css_class_on_selected_events(self):
        field = self.create_special_field(self.get_masterdata())
        self.create_event(**{'category': self.category,
                             'datetime': self.get_datetime(),
                             field.__name__: True})
        browser = self.get_browser('cal-exporter')
        browser.open(
            'http://localhost/ab/++attribute++calendar/@@export-month')
        self.assertEllipsis('''...
<dd>
  calendar-export-test
</dd>
...
<dd class="special">
  calendar-export-test
</dd>
...''', browser.contents)
