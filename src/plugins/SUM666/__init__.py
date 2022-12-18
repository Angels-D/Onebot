import os
import time
import locale
import json
from random import choice
from nonebot import get_driver
from nonebot import on_fullmatch
from nonebot import get_bot
from nonebot import logger
from nonebot.rule import Event
from nonebot.matcher import Matcher
from nonebot.adapters import Bot, Message
from nonebot.params import EventMessage
from .config import Config
try:
    from nonebot_plugin_rauthman import isInService
except Exception as e:
    logger.warning("功能管理(rauthman)模块加载失败:\n%s" % e)

plugin_config = Config.parse_obj(get_driver().config)
JSON_PATH = plugin_config.sum666_datapath
try:
    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
    File = open(JSON_PATH, 'r')
    Data = json.loads(File.read())
except Exception as e:
    logger.warning(e)
    File = open(JSON_PATH, 'w+')
    Data = dict()
File.close()


async def checker(event: Event) -> bool:
    session = event.get_session_id().split('_')
    return session[0] == "group" and \
        session[1] in plugin_config.sum666_group and \
        session[2] in plugin_config.sum666_user

sum666 = on_fullmatch(plugin_config.sum666_keyword, rule=checker & isInService("超级666", 1) if isInService else True, priority=50)


@sum666.handle()
async def sum666_handle(bot: Bot, matcher: Matcher, event: Event):
    global Data
    session = event.get_session_id().split('_')
    infos = await bot.get_group_member_info(group_id=session[1], user_id=session[2])
    key = session[1] + session[2]
    if key in Data.keys():
        Data[key] += 1
    else:
        Data[key] = 1
    File = open(JSON_PATH, 'w+')
    File.write(json.dumps(Data))
    File.close()
    await sum666.finish(choice(
        list(plugin_config.sum666_output)).format(
            infos['card'], session[2], Data[key], time.strftime('%H时%M分%S秒')
    ), at_sender=True
    )