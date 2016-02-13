from __future__ import unicode_literals
import pytest


@pytest.fixture(scope='function')
def master_data_menu(address_book, browser, sitemenu):
    """Fixture to test the calendar export master data menu."""
    browser.login('cal-export-editor')
    return sitemenu(browser, 1, 'Master data', browser.CALENDAR_MASTERDATA_URL)


def test_menu__master_data_menu__1(master_data_menu):
    """Asserting that the menu with the index 4 is calendar master data."""
    master_data_menu.assert_correct_menu_item_is_tested()


def test_menu__master_data_menu__2(master_data_menu):
    """The master data tab is selected on the export master data."""
    assert master_data_menu.item_selected(
        master_data_menu.browser.CALEXPORT_MASTER_DATA_URL)
