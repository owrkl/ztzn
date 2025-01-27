import asyncio
import contextlib
import os
import sys
from asyncio.exceptions import CancelledError
from time import sleep

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from . import UPSTREAM_REPO_URL, zedub

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _zedutils
from ..sql_helper.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)

plugin_category = "الادوات"
cmdhd = Config.COMMAND_HAND_LER
ENV = bool(os.environ.get("ENV", False))
LOGS = logging.getLogger(__name__)
# -- Constants -- #

OLDZED = Config.OLDZED

UPSTREAM_REPO_BRANCH = "master"

REPO_REMOTE_NAME = "temponame"
IFFUCI_ACTIVE_BRANCH_NAME = "master"
IS_SELECTED_DIFFERENT_BRANCH = (
    "looks like a custom branch {branch_name} "
    "is being used:\n"
    "in this case, Updater is unable to identify the branch to be updated."
    "please check out to an official branch, and re-start the updater."
)

# -- Constants End -- #

requirements_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    d_form = "%d/%m/%y"
    return "".join(
        f"  • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n"
        for c in repo.iter_commits(diff)
    )


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def update_bot(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    sandy = await event.edit(f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديث زدثــون\n**•─────────────────•**\n\n**•⎆┊تم التحـديث ⎌ بنجـاح**\n**•⎆┊جـارِ إعـادة تشغيـل بـوت زدثــون ⎋ **\n**•⎆┊انتظـࢪ مـن 2 - 1 دقيقـه . . .📟**")
    await event.client.reload(sandy)


@zedub.zed_cmd(
    pattern="تحديث البوت$",
)
async def upstream(event):
    if os.path.exists("config.py"):
        return await edit_delete(
            event,
            f"**- أعتقد أنك على الوضـع الذاتي ..**\n**- للتحديث الذاتي ارسـل الامـر** `{cmdhd}تحديث`",
        )
    event = await edit_or_reply(event, f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديث زدثــون\n**•─────────────────•**\n\n**⪼ يتم تنصيب التحديث  انتظر 🌐 ،**")
    off_repo = "https://github.com/ZThon-Back/ZUp"
    os.chdir("/setup")
    try:
        txt = (
            "`اووبـس .. لا يمكن لـ الإستمـرار بالتحديث بسبب "
            + "حـدوث بعـض المشاكـل`\n\n**سجـل الاخطـاء:**\n"
        )

        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n\n**- المسـار** {error} **غيـر مـوجـود؟!**")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n**- خطـأ غيـر متـوقـع؟!**\n{error}")
        return repo.__del__()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.main)
        repo.heads.master.set_tracking_branch(origin.refs.main)
        repo.heads.master.checkout(True)
    with contextlib.suppress(BaseException):
        repo.create_remote("upstream", off_repo)
    zzz1 = await event.edit(f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديث زدثــون\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**")
    await asyncio.sleep(1)
    zzz2 = await zzz1.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديث زدثــون\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟷𝟶 ▬▭▭▭▭▭▭▭▭▭")
    await asyncio.sleep(1)
    zzz3 = await zzz2.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديث زدثــون\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟸𝟶 ▬▬▭▭▭▭▭▭▭▭")
    await asyncio.sleep(1)
    zzz4 = await zzz3.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديث زدثــون\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟹𝟶 ▬▬▬▭▭▭▭▭▭▭")
    await asyncio.sleep(1)
    zzz5 = await zzz4.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديث زدثــون\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟺𝟶 ▬▬▬▬▭▭▭▭▭▭")
    await asyncio.sleep(1)
    zzz6 = await zzz5.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديث زدثــون\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟻𝟶 ▬▬▬▬▬▭▭▭▭▭")
    await asyncio.sleep(1)
    zzz7 = await zzz6.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديث زدثــون\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟼𝟶 ▬▬▬▬▬▬▭▭▭▭")
    await asyncio.sleep(1)
    zzz8 = await zzz7.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديث زدثــون\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟽𝟶 ▬▬▬▬▬▬▬▭▭▭")
    await asyncio.sleep(1)
    zzz9 = await zzz8.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديث زدثــون\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟾𝟶 ▬▬▬▬▬▬▬▬▭▭") 
    await asyncio.sleep(1)
    zzzz10 = await zzz9.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديث زدثــون\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟿𝟶 ▬▬▬▬▬▬▬▬▬▭") 
    await asyncio.sleep(1)
    zzzz11 = await zzzz10.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديث زدثــون\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟷𝟶𝟶 ▬▬▬▬▬▬▬▬▬▬💯") 
    ac_br = repo.active_branch.name
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    await update_bot(zzzz11, repo, ups_rem, ac_br)
