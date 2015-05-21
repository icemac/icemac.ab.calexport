import icemac.ab.calexport.testing


class RoleTests(icemac.ab.calexport.testing.ZCMLTestCase):
    """Testing ..roles."""

    def test_calexport_editor_is_in_editor_roles(self):
        from icemac.addressbook.principals.roles import has_editor_role
        self.assertTrue(has_editor_role(['icemac.ab.calexport.ExportEditor']))

    def test_calendar_exporter_is_in_visitor_roles(self):
        from icemac.addressbook.principals.roles import has_visitor_role
        self.assertTrue(has_visitor_role(['icemac.ab.calexport.Exporter']))
