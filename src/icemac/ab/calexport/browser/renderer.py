import grokcore.component as grok
import icemac.ab.calendar.browser.renderer.table


class ExportTable(icemac.ab.calendar.browser.renderer.table.Table):
    """Tabular export of a calendar."""

    grok.name('export-table')
    may_render_days_as_add_links = False
    render_event_adapter_name = 'export-event'


class ExportEvent(icemac.ab.calendar.browser.renderer.table.TableEvent):
    """Export the data of an event in a table."""

    default_text = u''  # Do not render events without title

    def action_url(self):
        return None

    def info(self):
        return []
