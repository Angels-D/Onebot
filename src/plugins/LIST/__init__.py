from nonebot import get_driver
from nonebot import on_command, on_fullmatch
from nonebot import logger
from nonebot.rule import Event
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import CommandArg, EventMessage
from nonebot import get_bot
from .config import Config
try:
    from nonebot_plugin_rauthman import isInService
except Exception as e:
    logger.warning("功能管理(rauthman)模块加载失败:\n%s" % e)

plugin_config = Config.parse_obj(get_driver().config)

STATUS = False
MSG_IN = ""
MSG_OUT = ""
USER = ""

Usage = """请输入正确的格式:
1. /排队 状态: 查询当前机器人状态
2. /排队 关: 关闭机器人排队
3. /排队 开 [检测消息] [发送消息]: 激活机器人排队"""


async def open_checker(event: Event) -> bool:
    session = event.get_session_id()
    for key in plugin_config.open_group:
        if key in session:
            return True
    return event.get_user_id() in plugin_config.open_user


async def target_checker(event: Event) -> bool:
    if STATUS:
        session = event.get_session_id()
        for key in plugin_config.target_group:
            if key in session:
                return True
    return False

open = on_command("open", rule=open_checker & isInService("排队", 1) if isInService else True, aliases={
                  "排队"}, priority=5)
target = on_fullmatch(plugin_config.default_keyword,
                      rule=target_checker, priority=50)


@open.handle()
async def open_handle(matcher: Matcher, args: Message = CommandArg()):
    global STATUS, MSG_IN, MSG_OUT
    plain_text = args.extract_plain_text().split(' ')
    if not args.extract_plain_text():
        await open.finish(Usage)
    elif plain_text[0] == '状态':
        if STATUS:
            await open.finish('排队: 开启 检测消息: %s 发送消息: %s' % (MSG_IN, MSG_OUT))
        else:
            await open.finish("排队: 关闭")
    elif plain_text[0] == '关':
        STATUS = False
        await open.finish("已停止排队")
    elif plain_text[0] == '开' and len(plain_text) == 3:
        MSG_IN, MSG_OUT = plain_text[1:3]
        STATUS = True
        await open.finish('排队: 开启 检测消息: %s 发送消息: %s' % (MSG_IN, MSG_OUT))
    else:
        await open.finish(Usage)


@target.handle()
async def target_handle(matcher: Matcher, args: Message = EventMessage()):
    if MSG_IN.replace(" ", "") == str(args).replace(" ", ""):
        global STATUS
        STATUS = False
        await target.send(MSG_OUT)
        await get_bot().call_api("send_group_msg", group_id=plugin_config.msg_group,
                                 message="%s 已排上" % (MSG_OUT)
                                 )
