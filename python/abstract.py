from telegram import Bot, InlineKeyboardMarkup
from telegram.ext import Application
from gspread import utils

import requests

from typing import Coroutine, Any

from spreadsheetbot.sheets.abstract import AbstractSheetAdapter

def _get_send_to_all_uids_coroutines(self: AbstractSheetAdapter, selector, app: Application, message: str, parse_mode: str, 
    send_photo: str = None, send_document: str = None, reply_markup: InlineKeyboardMarkup = None
) -> list[Coroutine[Any, Any, Any]]:
    bot: Bot = app.bot
    if send_photo not in [None, '']:
        return [
            bot.send_photo(chat_id=uid, photo=send_photo, caption=message, parse_mode=parse_mode, reply_markup=reply_markup)
            for uid in self.as_df.loc[selector][self.uid_col].to_list()
        ]
    if send_document not in [None, '']:
        responce = requests.get(send_document)
        responce.raise_for_status()
        filename = '__.pdf'
        if 'content-disposition' in responce.headers:
            filename = responce.headers['content-disposition'].removeprefix('attachment; filename=').replace('"', '')
        return [
            bot.send_document(
                chat_id=uid,
                document=responce.content,
                filename=filename,
                caption=message,
                parse_mode=parse_mode,
                reply_markup=reply_markup
            )
            for uid in self.as_df.loc[selector][self.uid_col].to_list()
        ]
    return [
        bot.send_message(chat_id=uid, text=message, parse_mode=parse_mode, reply_markup=reply_markup)
        for uid in self.as_df.loc[selector][self.uid_col].to_list()
    ]
AbstractSheetAdapter._get_send_to_all_uids_coroutines = _get_send_to_all_uids_coroutines

def _send_to_all_uids(self: AbstractSheetAdapter, selector, app: Application, message: str, parse_mode: str, 
    send_photo: str = None, send_document: str = None, reply_markup: InlineKeyboardMarkup = None
):
    update = self._create_update_context(
        'Send to all uids',
        message=message,
        parse_mode=parse_mode,
        send_photo=send_photo,
        send_document=send_document,
        reply_markup=reply_markup.to_dict() if reply_markup else reply_markup
    )
    for send_message in self._get_send_to_all_uids_coroutines(selector, app, message, parse_mode, send_photo, send_document, reply_markup):
        app.create_task(send_message, update)
AbstractSheetAdapter._send_to_all_uids = _send_to_all_uids

def _prepare_batch_update(self, rowcols: list[tuple[str|int]]) -> list[str]:
    return [{
        'range': utils.rowcol_to_a1(int(x[0]), int(x[1])),
        'values': [[x[2]]],
    } for x in rowcols ]
AbstractSheetAdapter._prepare_batch_update = _prepare_batch_update