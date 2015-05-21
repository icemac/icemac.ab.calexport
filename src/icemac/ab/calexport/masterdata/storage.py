import icemac.ab.calexport.interfaces
import icemac.ab.calendar.interfaces
import grokcore.annotation as grok


class ExportMasterData(grok.Annotation):
    """Store export master data in annotations."""

    grok.context(icemac.ab.calendar.interfaces.ICalendar)
    grok.implements(icemac.ab.calexport.interfaces.IExportMasterdata)
