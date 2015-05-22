import icemac.ab.calexport.testing


class MasterdataTests(icemac.ab.calexport.testing.BrowserTestCase):
    """Testing ..export.Masterdata."""

    def test_form_saves_data(self):
        self.create_category(u'foo')
        self.create_category(u'bar')
        browser = self.get_browser('cal-export-editor')
        browser.open('http://localhost/ab/@@calendar-masterdata.html')
        browser.getLink('Configure export').click()
        form_url = ('http://localhost/ab/++attribute++calendar/'
                    '@@edit-export-masterdata.html')
        self.assertEqual(form_url, browser.url)
        browser.getControl('HTML to be inserted above').value = '<html>cal'
        browser.getControl('foo').selected = True
        browser.getControl('Apply').click()
        self.assertEqual(['Data successfully updated.'],
                         browser.get_messages())
        browser.open(form_url)
        self.assertEqual('<html>cal',
                         browser.getControl('HTML to be inserted above').value)
        self.assertTrue(browser.getControl('foo').selected)
        self.assertFalse(browser.getControl('bar').selected)


class MasterdataSecurityTests(icemac.ab.calexport.testing.BrowserTestCase):
    """Security testing ..export.Masterdata."""

    def test_exporter_is_not_able_to_access_fields(self):
        from mechanize import LinkNotFoundError, HTTPError
        browser = self.get_browser('cal-exporter')
        browser.open('http://localhost/ab/@@calendar-masterdata.html')
        with self.assertRaises(LinkNotFoundError):
            browser.getLink('Configure export')
        # The URL is not accesible, too:
        with self.assertRaises(HTTPError) as err:
            browser.open('http://localhost/ab/++attribute++calendar/'
                         '@@edit-export-masterdata.html')
        self.assertEqual('HTTP Error 403: Forbidden', str(err.exception))
