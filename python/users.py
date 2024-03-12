from telegram.ext import Application

from spreadsheetbot.sheets.users import UsersAdapterClass

from spreadsheetbot.sheets.notifications import Notifications

def send_notification_to_all_users(self, app: Application, message: str, parse_mode: str,
                                    send_photo: str = None, send_document: str = None, state: str = None,
                                    condition: str = None):
    condition_column = 'is_active' if condition in [None, ''] else condition
    self._send_to_all_uids(
        self.selector_condition(condition_column),
        app, message, parse_mode,
        send_photo, send_document,
        reply_markup=Notifications.get_inline_keyboard_by_state(state)
    )
UsersAdapterClass.send_notification_to_all_users = send_notification_to_all_users