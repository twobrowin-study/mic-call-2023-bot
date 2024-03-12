import os, sys, json, dotenv
from spreadsheetbot import SpreadSheetBot, Log, DEBUG
from spreadsheetbot.spreadsheetbot import HELP_COMMAND

from telegram import Bot
from telegram.ext import Application

from spreadsheetbot.sheets.i18n import I18n
from spreadsheetbot.sheets.switch import Switch
from spreadsheetbot.sheets.settings import Settings
from spreadsheetbot.sheets.registration import Registration
from spreadsheetbot.sheets.log import LogSheet
from spreadsheetbot.sheets.groups import Groups
from spreadsheetbot.sheets.users import Users
from spreadsheetbot.sheets.report import Report
from spreadsheetbot.sheets.keyboard import Keyboard
from spreadsheetbot.sheets.notifications import Notifications

import abstract
import groups
import users

from reschedule import PerformAndScheldueNotifications

if "DOCKER_RUN" in os.environ:
    Log.info("Running in docker environment")
else:
    dotenv.load_dotenv(dotenv.find_dotenv())
    Log.info("Running in dotenv environment")

if len(sys.argv) > 1 and sys.argv[1] in ['debug', '--debug', '-D']:
    Log.setLevel(DEBUG)
    Log.debug("Starting in debug mode")

BOT_TOKEN            = os.environ.get('BOT_TOKEN')
SHEETS_ACC_JSON      = json.loads(os.environ.get('SHEETS_ACC_JSON'))
SHEETS_LINK          = os.environ.get('SHEETS_LINK')
SWITCH_UPDATE_TIME   = int(os.environ.get('SWITCH_UPDATE_TIME'))
SETTINGS_UPDATE_TIME = int(os.environ.get('SETTINGS_UPDATE_TIME'))

async def post_init(self, app: Application) -> None:
    Switch.set_sleep_time(self.switch_update_time)
    Settings.set_sleep_time(self.setting_update_time)

    await I18n.async_init(self.sheets_secret, self.sheets_link)
    await LogSheet.async_init(self.sheets_secret, self.sheets_link)
    await Switch.async_init(self.sheets_secret, self.sheets_link)
    await Settings.async_init(self.sheets_secret, self.sheets_link)
    await Groups.async_init(self.sheets_secret, self.sheets_link)
    await Users.async_init(self.sheets_secret, self.sheets_link)
    await Registration.async_init(self.sheets_secret, self.sheets_link)
    await Report.async_init(self.sheets_secret, self.sheets_link)
    await Keyboard.async_init(self.sheets_secret, self.sheets_link)
    await Notifications.async_init(self.sheets_secret, self.sheets_link)

    bot: Bot = app.bot
    await bot.set_my_commands([(HELP_COMMAND, Settings.help_command_description)])
    
    my_name = await bot.get_my_name()
    if my_name.name != Settings.my_name:
        await bot.set_my_name(Settings.my_name)
    
    my_short_description = await bot.get_my_short_description()
    if my_short_description.short_description  != Settings.my_short_description:
        await bot.set_my_short_description(Settings.my_short_description)
    
    my_description = await bot.get_my_description()
    if my_description.description  != Settings.my_description:
        await bot.set_my_description(Settings.my_description)

    await LogSheet.write(None, "Started an application")

    Switch.scheldue_update(app)
    Settings.scheldue_update(app)
    Groups.scheldue_update(app)
    Users.scheldue_update(app)
    Registration.scheldue_update(app)
    Report.scheldue_update(app)
    Keyboard.scheldue_update(app)
    PerformAndScheldueNotifications(app)
SpreadSheetBot.post_init = post_init 

if __name__ == "__main__":
    bot = SpreadSheetBot(
        BOT_TOKEN,
        SHEETS_ACC_JSON,
        SHEETS_LINK,
        SWITCH_UPDATE_TIME,
        SETTINGS_UPDATE_TIME
    )
    bot.run_polling()