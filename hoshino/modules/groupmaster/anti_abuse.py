# TODO: rewrite this


import random
from datetime import timedelta

from nonebot import on_command
from nonebot.message import _check_calling_me_nickname

import hoshino
from hoshino import R, util, trigger
from hoshino.typing import CQEvent, Union
from aiocqhttp import Message
'''
from nonebot.command import CommandManager
def parse_command(bot, cmd_str):
    parse_command = CommandManager().parse_command(bot, cmd_str)


bot = nonebot.get_bot()
BLANK_MESSAGE = Message(MessageSegment.text(''))

@message_preprocessor
async def black_filter(bot, ctx, plugin_manager=None):  # plugin_manager is new feature of nonebot v1.6
    first_msg_seg = ctx['message'][0]
    if first_msg_seg.type == 'hb':
        return  # pass normal Luck Money Pack to avoid abuse
    if ctx['message_type'] == 'group' and hoshino.priv.check_block_group(ctx['group_id']) \
       or hoshino.priv.check_block_user(ctx['user_id']):
        ctx['message'] = BLANK_MESSAGE


def _check_hbtitle_is_cmd(ctx, title):
    ctx = ctx.copy()    # 复制一份，避免影响原有的ctx
    ctx['message'] = Message(title)
    _check_calling_me_nickname(bot, ctx)
    cmd, _ = parse_command(bot, str(ctx['message']).lstrip())
    return bool(cmd)


@bot.on_message('group')
async def hb_handler(ctx):
    self_id = ctx['self_id']
    user_id = ctx['user_id']
    group_id = ctx['group_id']
    first_msg_seg = ctx['message'][0]
    if first_msg_seg.type == 'hb':
        title = first_msg_seg['data']['title']
        if _check_hbtitle_is_cmd(ctx, title):
            hoshino.priv.set_block_group(group_id, timedelta(hours=1))
            hoshino.priv.set_block_user(user_id, timedelta(days=30))
            await util.silence(ctx, 7 * 24 * 60 * 60)
            msg_from = f"{ctx['user_id']}@[群:{ctx['group_id']}]"
            hoshino.logger.critical(f'Self: {ctx["self_id"]}, Message {ctx["message_id"]} from {msg_from} detected as abuse: {ctx["message"]}')
            await bot.send(ctx, "检测到滥用行为，您的操作已被记录并加入黑名单。\nbot拒绝响应本群消息1小时", at_sender=True)
            try:
                await bot.set_group_kick(self_id=self_id, group_id=group_id, user_id=user_id, reject_add_request=True)
                hoshino.logger.critical(f"已将{user_id}移出群{group_id}")
            except:
                pass

'''
from nonebot.command import CommandManager


def parse_command(bot, cmd_str, NOTLOG=False):
    parse_command = CommandManager().parse_command(bot, cmd_str, NOTLOG)
    return parse_command


using_cmd_msg = {}


def check_command(msg) -> str:
    if type(msg) is str:
        message = Message(msg)
        rmessage = msg
    elif type(msg) is CQEvent:
        message = msg.message
        rmessage = msg.raw_message
        msg = msg.raw_message
    else:
        return None
    if msg in using_cmd_msg:
        return using_cmd_msg[msg]
    ev = {
        "message":  message,
        "message_type": "group",
        "post_type": "message",
        "raw_message": rmessage,
        "sub_type": "normal",
        }
    event = CQEvent().from_payload(ev)
    event['to_me'] = False
    _check_calling_me_nickname(hoshino.get_bot(), event)
    for t in trigger.chain:
        if sf := t.find_handler(event):
            if sf.only_to_me and not event['to_me']:
                continue
            using_cmd_msg[msg] = t.__class__.__name__
            return t.__class__.__name__
    cmd_str = event.plain_text
    cmd, _ = parse_command(hoshino.get_bot(), cmd_str=cmd_str, NOTLOG=True)
    if cmd:
        using_cmd_msg[msg] = str(cmd.name)
        return str(cmd.name)

# ============================================ #


BANNED_WORD = (
    'rbq', 'RBQ', '憨批', '废物', '死妈', '崽种', '傻逼', '傻逼玩意',
    '没用东西', '傻B', '傻b', 'SB', 'sb', '煞笔', 'cnm', '爬', 'kkp',
    'nmsl', 'D区', '口区', '我是你爹', 'nmbiss', '弱智', '给爷爬', '杂种爬',
    '爪巴'
)


@on_command('ban_word', aliases=BANNED_WORD, only_to_me=True)
async def ban_word(session):
    ctx = session.ctx
    user_id = ctx['user_id']
    msg_from = str(user_id)
    if ctx['message_type'] == 'group':
        msg_from += f'@[群:{ctx["group_id"]}]'
        if hoshino.priv.check_block_group(ctx["group_id"]):
            return
    elif ctx['message_type'] == 'discuss':
        msg_from += f'@[讨论组:{ctx["discuss_id"]}]'
    hoshino.logger.critical(
        f'Self: {ctx["self_id"]}, Message {ctx["message_id"]} from {msg_from}: {ctx["message"]}')
    hoshino.priv.set_block_user(user_id, timedelta(hours=8))
    pic = R.img(f"kkl/badword{random.randint(1, 4)}.jpg").cqcode
    await session.send(f"不理你啦！バーカー\n{pic}", at_sender=True)
    await util.silence(session.ctx, 8*60*60, skip_su=False)

bot = hoshino.get_bot()


@bot.on_message('group')
async def hb_handler(ev: CQEvent):
    for m in ev.message:
        if m['type'] == 'redbag':
            print(ev)
            title = m['data']['title']
            break
    else:
        return
    if title:
        if check_command(title):
            group_id = ev.group_id
            user_id = ev.user_id
            self_id = ev.self_id
            hoshino.priv.set_block_group(group_id, timedelta(hours=1))
            hoshino.priv.set_block_user(user_id, timedelta(days=30))
            msg_from = f"{user_id}@[群:{group_id}]"
            hoshino.logger.critical(
                f'Self: {self_id}, Message {ev["message_id"]} from {msg_from} detected as abuse: {ev.message}')
            pic = R.img('kkl/zhenhankkl2.jpg').cqcode
            await hoshino.get_bot().send(ev, f"{pic}\n检测到滥用行为，您的操作已被记录并加入黑名单。\nbot拒绝响应本群消息1小时")
