import icemac.ab.calexport.testing


class MasterdataTests(icemac.ab.calexport.testing.BrowserTestCase):
    """Testing ..export.Masterdata."""

    def test_(self):
        pass


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
