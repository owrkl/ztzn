import asyncio
import contextlib
import os
import sys
from asyncio.exceptions import CancelledError
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
UPSTREAM_REPO_BRANCH = "master"

requirements_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt"
)


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            f"{sys.executable} -m pip install -r {reqs}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def deploy(event, repo, ups_rem, ac_br, txt):
    """Deploy using Render's Git-based approach."""
    try:
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        # Assuming a Render-compatible branch (e.g., `main`)
        ups_rem.push(refspec="HEAD:refs/heads/main", force=True)
    except GitCommandError as error:
        await event.edit(f"{txt}\n**Error log:**\n`{error}`")
        return repo.__del__()
    
    await event.edit("🚀 **Deployment initiated successfully!**\n"
                     "Render.com will handle the build and deployment process.")
    # Simulate Render's deployment status by disconnecting
    with contextlib.suppress(CancelledError):
        await event.client.disconnect()


@zedub.zed_cmd(
    pattern="تحديث البوت$",
)
async def upstream(event):
    """Update the bot with the latest changes from the upstream repository."""
    event = await edit_or_reply(event, "🔄 **Updating from upstream repository...**")
    off_repo = "https://github.com/ZThon-Back/ZUp"
    os.chdir("/app")
    try:
        repo = Repo()
    except NoSuchPathError as error:
        return await event.edit(f"❌ Path error: {error}")
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.main)
        repo.heads.master.set_tracking_branch(origin.refs.main)
        repo.heads.master.checkout(True)

    with contextlib.suppress(BaseException):
        repo.create_remote("upstream", off_repo)
    
    ups_rem = repo.remote("upstream")
    ac_br = repo.active_branch.name
    ups_rem.fetch(ac_br)
    txt = "Error during deployment."

    await deploy(event, repo, ups_rem, ac_br, txt)
