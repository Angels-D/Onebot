import time
import json
import requests
from random import choice
from nonebot import get_driver
from nonebot import on_command
from nonebot import get_bot
from nonebot import logger
from nonebot.rule import Event
from nonebot.matcher import Matcher
from nonebot.adapters import Bot, Message
from nonebot.params import EventMessage, CommandArg
from .config import Config
try:
    from nonebot_plugin_rauthman import isInService
except Exception as e:
    logger.warning("功能管理(rauthman)模块加载失败:\n%s" % e)

plugin_config = Config.parse_obj(get_driver().config)

LAST_TIME = 0


async def checker(event: Event) -> bool:
    session = event.get_session_id().split('_')
    return session[0] != "group" or \
        session[1] in plugin_config.chatgpt_group

chatgpt = on_command("GPT", rule=checker & isInService(
    "ChatGpt", 1) if isInService else True, aliases={"对话"}, priority=5)


@chatgpt.handle()
async def chatgpt_handle(bot: Bot, matcher: Matcher, event: Event, args: Message = CommandArg()):
    global LAST_TIME
    plain_text = args.extract_plain_text()
    CD_TIME = int(plugin_config.chatgpt_cd_time + LAST_TIME - time.time())
    if (CD_TIME > 0):
        await chatgpt.finish("ChatGPT冷却中, 还有%d秒" % CD_TIME, at_sender=True)
    if (not plain_text):
        await chatgpt.finish("您想说些什么", at_sender=True)
    try:
        request = requests.get('http://chat.h2ai.cn/api/trilateral/openAi/completions?prompt=%s&openaiId=%s' %
                               (plain_text, choice(list(plugin_config.chatgpt_openid))))
        data = json.loads(request.text)['data']['choices'][0]['text']
    except Exception as e:
        await chatgpt.finish(AT + "===== ChatGPT回复失败, 请联系管理员 =====\n" + e + "\n========================================", at_sender=True)
    else:
        LAST_TIME = time.time()
        await chatgpt.finish(data.replace("<br/>", "\n"), at_sender=True)
