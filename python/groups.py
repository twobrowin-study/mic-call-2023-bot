from telegram.ext import Application

from spreadsheetbot.sheets.groups import GroupsAdapterClass

from spreadsheetbot.sheets.i18n import I18n

def send_to_all_normal_groups(self, app: Application, message: str, parse_mode: str, send_photo: str = None,  send_document: str = None):
    self._send_to_all_uids(
        self.as_df.is_admin == I18n.no,
        app, message, parse_mode, send_photo, send_document
    )
GroupsAdapterClass.send_to_all_normal_groups = send_to_all_normal_groups

def send_to_all_admin_groups(self, app: Application, message: str, parse_mode: str, send_photo: str = None,  send_document: str = None):
    self._send_to_all_uids(
        self.as_df.is_admin.isin(I18n.yes_super),
        app, message, parse_mode, send_photo, send_document
    )
GroupsAdapterClass.send_to_all_admin_groups = send_to_all_admin_groups

def send_to_all_superadmin_groups(self, app: Application, message: str, parse_mode: str, send_photo: str = None,  send_document: str = None):
    self._send_to_all_uids(
        self.as_df.is_admin == I18n.super,
        app, message, parse_mode, send_photo, send_document
    )
GroupsAdapterClass.send_to_all_superadmin_groups = send_to_all_superadmin_groups

async def async_send_to_all_superadmin_groups(self, app: Application, message: str, parse_mode: str, send_photo: str = None,  send_document: str = None):
    for send_message_continue in self._get_send_to_all_uids_coroutines(
        self.as_df.is_admin == I18n.super,
        app, message, parse_mode, send_photo, send_document
    ):
        await send_message_continue
GroupsAdapterClass.async_send_to_all_superadmin_groups = async_send_to_all_superadmin_groups