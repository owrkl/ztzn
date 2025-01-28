import asyncio
import os
import sys
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from . import zedub
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply

cmdhd = Config.COMMAND_HAND_LER
OFF_REPO_URL = "https://github.com/ZThon-Back/ZUp"
REPO_PATH = os.path.join(os.getcwd(), "app")


async def update_requirements():
    """Update Python requirements."""
    try:
        process = await asyncio.create_subprocess_shell(
            f"{sys.executable} -m pip install -r requirements.txt",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def show_progress(event, current, total):
    """Show the progress bar."""
    progress = int((current / total) * 100)
    bar = "▬" * (progress // 10) + "▭" * (10 - (progress // 10))
    await event.edit(
        f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديث زدثــون\n"
        "**•─────────────────•**\n\n"
        f"⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐\n\n"
        f"%{progress} {bar}"
    )


async def update_bot(event, repo, ups_rem, ac_br):
    """Pull updates from the repository and reload the bot."""
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    await event.edit(
        "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديث زدثــون\n"
        "**•─────────────────•**\n\n"
        "**•⎆┊تم التحـديث ⎌ بنجـاح**\n"
        "**•⎆┊جـارِ إعـادة تشغيـل بـوت زدثــون ⎋**\n"
        "**•⎆┊انتظـࢪ مـن 2 - 1 دقيقـه . . .📟**"
    )
    await event.client.reload()


@zedub.zed_cmd(pattern="تحديث البوت$")
async def upstream(event):
    """Handle bot update command."""
    if os.path.exists("config.py"):
        return await edit_delete(
            event,
            f"**- أعتقد أنك على الوضـع الذاتي ..**\n"
            f"**- للتحديث الذاتي ارسـل الامـر** `{cmdhd}تحديث`",
        )

    event = await edit_or_reply(
        event,
        "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديث زدثــون\n"
        "**•─────────────────•**\n\n"
        "⏳ يتم تنصيب التحديث  انتظر 🌐",
    )

    # Ensure repository directory exists
    if not os.path.exists(REPO_PATH):
        os.makedirs(REPO_PATH)
    os.chdir(REPO_PATH)

    # Initialize or fetch repository
    try:
        repo = Repo(REPO_PATH)
    except (InvalidGitRepositoryError, NoSuchPathError):
        repo = Repo.init(REPO_PATH)
        origin = repo.create_remote("upstream", OFF_REPO_URL)
        origin.fetch()
        default_branch = "main" if "main" in [ref.name for ref in origin.refs] else "master"
        repo.create_head(default_branch, origin.refs[default_branch])
        repo.heads[default_branch].set_tracking_branch(origin.refs[default_branch])
        repo.heads[default_branch].checkout()
    except GitCommandError as error:
        await event.edit(f"❌ خطأ في Git:\n{error}")
        return

    # Display progress bar
    for i in range(11):
        await asyncio.sleep(1)  # Simulate progress delay
        await show_progress(event, i, 10)

    # Pull updates and reload bot
    try:
        ups_rem = repo.remote("upstream")
        ac_br = repo.active_branch.name
        ups_rem.fetch(ac_br)
        await update_bot(event, repo, ups_rem, ac_br)
    except Exception as e:
        await event.edit(f"❌ حدث خطأ أثناء التحديث:\n{e}")
