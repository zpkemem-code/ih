import asyncio
import os
import traceback
from datetime import datetime

import croniter
from aiorun import run
from pyrogram.errors import (AuthKeyDuplicated, AuthKeyUnregistered,
                             SessionRevoked, UserAlreadyParticipant,
                             UserDeactivated, UserDeactivatedBan)
from pytz import timezone

from config import LOG_SELLER, OWNER_ID
from Zohun import UserBot, bot, logger, zohun
from Zohun.database import dB
from Zohun.helpers import (AutoBC, CheckSellerCount, CheckUsers, CleanAcces,
                          ExpiredUser, ReadUser, Tools, check_payment,
                          installPeer)

list_error = []


async def cleanup_total(ubot_id):
    """Clean up database records for a specific userbot."""
    try:
        await dB.remove_ubot(ubot_id)
        logger.info(f"Deleted user {ubot_id}")
    except Exception as e:
        logger.error(f"Failed to cleanup userbot {ubot_id}: {e}")


async def auto_restart():
    tz = timezone("Asia/Jakarta")
    cron = croniter.croniter("45 01 * * *", datetime.now(tz))
    while True:
        now = datetime.now(tz)
        next_run = cron.get_next(datetime)

        wait_time = (next_run - now).total_seconds()
        await asyncio.sleep(wait_time)
        try:
            await bot.send_message(
                OWNER_ID,
                "<blockquote><b>Restart Daily..\n\nTunggu beberapa menit bot sedang di Restart!!</b></blockquote>",
            )
            await stop_main()
            os.execl("/bin/bash", "bash", "start.sh")
        except Exception as e:
            logger.error(f"Error during restart: {e}")


async def send_safe_message(chat_id, text):
    """Send message with proper error handling."""
    try:
        await bot.send_message(chat_id, text)
        return True
    except Exception as e:
        logger.error(f"Failed to send message to {chat_id}: {e}")
        return False


async def handle_start_error():
    """Handle startup errors with safe message sending."""
    if list_error:
        for data in list_error:
            ubot = data["user"]
            reason = data["error_msg"]
            
            error_message = f"<b>Userbot {ubot} failed to start due to {reason}, deleted user on database</b>"
            
            # Try sending to LOG_SELLER first
            success = await send_safe_message(LOG_SELLER, error_message)
            
            # If failed, try sending to OWNER_ID as fallback
            if not success:
                await send_safe_message(OWNER_ID, error_message)
            
            await cleanup_total(ubot)


async def start_ubot(ubot):
    """Start a userbot instance and handle setup."""
    userbot = UserBot(**ubot)
    try:
        await userbot.start()
        await asyncio.sleep(2)
        
        # Join required chats
        required_chats = ["ZonaHunterCH", "ZonaHunterNew", "warungrimnew"]
        for chat in required_chats:
            try:
                await userbot.get_chat(chat)
                await asyncio.sleep(0.5)
                await userbot.join_chat(chat)
                await asyncio.sleep(1)
                logger.info(f"✅ Successfully joined {chat} for userbot {ubot['name']}")
            except UserAlreadyParticipant:
                logger.info(f"ℹ️ Userbot {ubot['name']} already in {chat}")
                pass
            except Exception as e:
                logger.warning(f"⚠️ Could not join chat {chat} for userbot {ubot['name']}: {e}")
                continue
                
        return True
        
    except (AuthKeyUnregistered, AuthKeyDuplicated, SessionRevoked):
        reason = "Session Ended"
        data = {"user": int(ubot["name"]), "error_msg": reason}
        list_error.append(data)
        try:
            await userbot.stop()
        except Exception as e:
            logger.error(f"Error stopping userbot {ubot['name']}: {e}")
        return False
        
    except (UserDeactivated, UserDeactivatedBan):
        reason = "Account Banned by Telegram"
        data = {"user": int(ubot["name"]), "error_msg": reason}
        list_error.append(data)
        try:
            await userbot.stop()
        except Exception as e:
            logger.error(f"Error stopping userbot {ubot['name']}: {e}")
        return False
        
    except Exception as e:
        logger.error(f"Unexpected error starting userbot {ubot['name']}: {e}")
        return False


async def start_main_bot():
    """Start the main bot after userbots."""
    logger.info("🤖 Starting main bot...")
    await bot.start()
    await bot.add_reseller()
    total_bots = len(zohun._ubot)
    message = f"🔥**Userbot berhasil diaktifkan**🔥\n✅ **Total User: {total_bots}**"
    await dB.set_var(bot.id, "total_users", total_bots)
    logger.info("✅ Main bot started successfully.")
    
    # Send startup message with error handling
    success = await send_safe_message(OWNER_ID, f"<blockquote>{message}</blockquote>")
    if not success:
        logger.warning("Failed to send startup message to OWNER_ID")


async def start_userbots():
    """Initialize and start all userbots."""
    await dB.initialize()
    logger.info("🔄 Starting userbots...")
    userbots = await dB.get_userbots()
    logger.info(f"📊 Loaded {len(userbots)} userbots from database")
    
    if not userbots:
        logger.warning("⚠️ No userbots found in database")
        return

    tasks = [asyncio.create_task(start_ubot(ubot)) for ubot in userbots]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    successful = 0
    failed = 0
    
    for idx, result in enumerate(results):
        userbot_id = userbots[idx]['name']
        if isinstance(result, Exception):
            logger.error(f"❌ Error starting userbot {userbot_id}: {result}")
            failed += 1
        elif result is True:
            successful += 1
            logger.info(f"✅ Userbot {userbot_id} started successfully")
        else:
            failed += 1
            logger.warning(f"⚠️ Userbot {userbot_id} failed to start")

    logger.info(f"📊 Userbots startup summary: {successful} successful, {failed} failed")

    # Send summary to owner if there are failures
    if failed > 0:
        summary_message = (
            f"📊 **Userbots Startup Summary**\n"
            f"✅ Successful: {successful}\n"
            f"❌ Failed: {failed}\n"
            f"📝 Check logs for details."
        )
        await send_safe_message(OWNER_ID, summary_message)


async def end_main():
    """Start background tasks."""
    background_tasks = [
        ExpiredUser(),
        CheckSellerCount(),
        installPeer(),
        CheckUsers(),
        CleanAcces(),
        check_payment(),
        auto_restart(),
    ]
    
    for task in background_tasks:
        asyncio.create_task(task)
        
    logger.info(f"🔄 Started {len(background_tasks)} background tasks")


async def stop_main():
    """Clean shutdown procedure."""
    logger.info("🛑 Starting shutdown sequence...")
    
    # Get all running tasks except current one
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    logger.info(f"📌 Total tasks to stop: {len(tasks)}")

    if not tasks:
        logger.info("✅ No running tasks found.")
        return

    # Cancel all tasks
    for task in tasks:
        if not task.done():
            task.cancel()

    await asyncio.sleep(1)

    # Wait for tasks to complete cancellation
    for task in tasks:
        try:
            result = await asyncio.wait_for(asyncio.shield(task), timeout=5)
            logger.debug(f"Task completed: {task.get_name() or task}")
        except asyncio.TimeoutError:
            logger.warning(f"⏳ Timeout stopping task: {task.get_name() or task}")
        except asyncio.CancelledError:
            logger.debug(f"Task cancelled: {task.get_name() or task}")
        except Exception as e:
            logger.error(f"⚠️ Error in task {task.get_name() or task}: {e}")

    # Close database connections
    logger.info("🗄️ Closing database connections...")
    try:
        await Tools.close_fetch()
        await dB.close()
        logger.info("✅ Database connections closed successfully.")
    except Exception as e:
        logger.error(f"❌ Error closing database: {e}")

    logger.info("✅ Shutdown sequence completed.")


async def main():
    """Main application entry point."""
    try:
        # Debug information
        logger.info(f"🔧 Configuration Debug:")
        logger.info(f"   OWNER_ID: {OWNER_ID}")
        logger.info(f"   LOG_SELLER: {LOG_SELLER}")
        
        # Start the application
        await start_userbots()
        await start_main_bot()
        await ReadUser()
        await AutoBC()
        await end_main()
        await handle_start_error()
        
        logger.info("🎉 Application started successfully!")
        
        # Keep the application running
        while True:
            await asyncio.sleep(3600)  # Sleep for 1 hour
            
    except asyncio.CancelledError:
        logger.warning("🛑 Application stopped by cancellation.")
    except KeyboardInterrupt:
        logger.info("🛑 Application stopped by user interrupt.")
    except Exception as e:
        logger.error(f"💥 Critical error in main: {e}")
        logger.error(traceback.format_exc())
        
        # Try to notify owner about critical error
        try:
            error_msg = f"💥 **Critical Error in Main Application**\n\n`{str(e)}`"
            await send_safe_message(OWNER_ID, error_msg)
        except Exception as notify_error:
            logger.error(f"Failed to send error notification: {notify_error}")


if __name__ == "__main__":
    logger.info("🚀 Starting Zohun Ubot...")
    run(
        main(),
        loop=bot.loop,
        shutdown_callback=stop_main(),
    )