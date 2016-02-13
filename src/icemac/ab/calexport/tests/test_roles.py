from icemac.addressbook.principals.roles import has_editor_role
from icemac.addressbook.principals.roles import has_visitor_role


def test_roles__1(zcmlS):
    """The calendar export editor role is registered as an editor role."""
    assert has_editor_role(['icemac.ab.calexport.ExportEditor'])


def test_roles__2(zcmlS):
    """The calendar exporter role is registered as an visitor role."""
    assert has_visitor_role(['icemac.ab.calexport.Exporter'])
