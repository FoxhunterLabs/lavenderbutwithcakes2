from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ConnectorResult:
    observations: int
    evidence: int
    notes: List[str]


class BaseConnector:
    name: str = "base"

    def sync(self, connector_id: str, config: Dict[str, Any]) -> ConnectorResult:
        raise NotImplementedError


class ImportOnlyConnector(BaseConnector):
    """
    Import-only connector. Never reads external systems.
    """
    name = "import_only"
    note = "Import-only connector."

    def sync(self, connector_id: str, config: Dict[str, Any]) -> ConnectorResult:
        return ConnectorResult(0, 0, [self.note])


class SMSiMessageImportConnector(ImportOnlyConnector):
    name = "sms_imessage_import"
    note = "Import-only. Use /api/import_batch with connector=sms_imessage_import or UI upload."


class EmailImportConnector(ImportOnlyConnector):
    name = "email_import"
    note = "Import-only. Use /api/import_batch with connector=email_import."


class SlackImportConnector(ImportOnlyConnector):
    name = "slack_import"
    note = "Import-only. Use /api/import_batch with connector=slack_import."


class TeamsImportConnector(ImportOnlyConnector):
    name = "teams_import"
    note = "Import-only. Use /api/import_batch with connector=teams_import."


class CalendarImportConnector(ImportOnlyConnector):
    name = "calendar_import"
    note = "Import-only. Use /api/import_batch with connector=calendar_import."
