from __future__ import unicode_literals
import icemac.ab.calexport.testing
import icemac.addressbook.browser.testing


class MasterDataSelectedCheckerTests(
        icemac.addressbook.browser.testing.SiteMenuTestMixIn,
        icemac.ab.calexport.testing.BrowserTestCase):
    """Testing ..menu.export_views"""

    menu_item_index = 1
    menu_item_title = 'Master data'
    menu_item_URL = 'http://localhost/ab/@@calendar-masterdata.html'
    login_as = 'cal-export-editor'

    def test_master_data_tab_is_selected_on_export_masterdata(self):
        self.browser.open('http://localhost/ab/++attribute++calendar/'
                          '@@edit-export-masterdata.html')
        self.assertIsSelected()
