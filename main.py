import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from discord import Embed
from test import test_site
from span import test_signup_button
from pricing import test_pricing_button
from login import test_login_button
from startButton import test_google_button
from emailControl import selenium_test_email
from demo2 import selenium_test_demo_button

load_dotenv()
scheduler = AsyncIOScheduler()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

def setup_scheduler():
    
    scheduler.add_job(send_message, 'interval', minutes=1)
    print("Scheduler jobs are set.")

async def run_test_site():
    await run_test(test_site)

async def run_test_signup_button():
    await run_test(test_signup_button)

async def run_test_pricing_button():
    await run_test(test_pricing_button)

async def run_test_login_button():
    await run_test(test_login_button)

async def run_test_google_button():
    await run_test(test_google_button)

async def run_test_email():
    await run_test(selenium_test_email)

async def run_test_demo():
    await run_test(selenium_test_demo_button)



@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("Bot is now online.")
    if not scheduler.running:
        setup_scheduler()
        scheduler.start()


async def send_error(channel, filename):
    await channel.send(file=discord.File(filename))

async def run_test(test_func):
    print(f"About to run test: {test_func.__name__}")
    try:
        result = await asyncio.get_event_loop().run_in_executor(None, test_func)
        print(f"Test result for {test_func.__name__}: {result}")
        return result
    except Exception as e:
        print(f"Error running test {test_func.__name__}: {e}")
        return None, None
    
async def run_all_tests():
    print("Running all scheduled tests...")
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("Channel not found.")
        return

    all_works = True
    error_messages = []

    # Run each test and collect results
    test_results = [
        await run_test(test_site),
        await run_test(test_signup_button),
        await run_test(test_pricing_button),
        await run_test(test_login_button),
        await run_test(test_google_button),
        await run_test(selenium_test_email),
        await run_test(selenium_test_demo_button),
    ]

    # Process results
    for test_result, screenshot_path in test_results:
        if test_result is None or "works well" not in test_result:
            all_works = False
            error_messages.append(test_result)
            if screenshot_path:
                await send_error(channel, screenshot_path)

    # Send summary message
    if all_works:
        await channel.send("All tests passed successfully!")
    else:
        error_summary = "\n".join(error_messages)
        await channel.send(f"Some tests failed:\n{error_summary}")

    print("All scheduled tests have been run and messages sent.")


async def send_message():
    print("Running scheduled tests...")
    all_works = True
    channel = bot.get_channel(CHANNEL_ID)
    
    if channel:
        test_result, screenshot_path = await run_test(test_site)
        if test_result is None:
            print("An error occurred during the test.")
        if "WebSite is working well" not in test_result:
            await channel.send(test_result)
            if screenshot_path: 
                all_works = False
                await send_error(channel, screenshot_path)
        
        signup_result, signup_screenshot_path = await run_test(test_signup_button)
        if "Sign Up button works well" not in signup_result:
            await channel.send(signup_result)
            if signup_screenshot_path:
                all_works = False
                await send_error(channel, signup_screenshot_path)
        
        login_result, login_screenshot_path = await run_test(test_login_button)
        if "Login button works well" not in login_result:
            await channel.send(login_result)
            if login_screenshot_path:
                all_works = False
                await send_error(channel, login_screenshot_path)
        
        pricing_result, pricing_screenshot_path = await run_test(test_pricing_button)
        if "Pricing button works well" not in pricing_result:
            await channel.send(pricing_result)
            if pricing_screenshot_path:
                all_works = False
                await send_error(channel, pricing_screenshot_path)
        
        google_result, google_screenshot_path = await run_test(test_google_button)
        if "Google button works well" not in google_result:
            await channel.send(google_result)
            if google_screenshot_path:
                all_works = False
                await send_error(channel, google_screenshot_path)
        
        email_result, email_screenshot_path = await run_test(selenium_test_email)
        if "Email button works well" not in email_result:
            await channel.send(email_result)
            if email_screenshot_path:
                all_works = False
                await send_error(channel, email_screenshot_path)
        
        demo_result, demo_screenshot_path = await run_test(selenium_test_demo_button)
        if "Demo, mic and camera buttons are works well" not in demo_result:
            await channel.send(demo_result)
            if demo_screenshot_path:
                all_works = False
                await send_error(channel, demo_screenshot_path)
        
        if all_works:
            embed = Embed(title="Total Test Result", description="All tests passed!", color=0x00ff00)
            embed.add_field(name="Status", value="No problem on Perculus", inline=False)
            await channel.send(embed=embed)



async def sendError():
    print("Checking for errors...")
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        test_result, screenshot_path = await run_test(test_site)
        if "WebSite is working well" not in test_result:
            await channel.send(test_result)
            if screenshot_path: 
                await send_error(channel, screenshot_path)  

        signup_result, signup_screenshot_path = await run_test(test_signup_button)
        if "Sign Up button works well" not in signup_result:
            await channel.send(signup_result)
            if signup_screenshot_path:  
                await send_error(channel, signup_screenshot_path)

        pricing_result, pricing_screenshot_path = await run_test(test_pricing_button)
        if "Pricing button works well" not in pricing_result:
            await channel.send(pricing_result)
            if pricing_screenshot_path:  
                await send_error(channel, pricing_screenshot_path)

        login_result, login_screenshot_path = await run_test(test_login_button)
        if "Login button works well" not in login_result:
            await channel.send(login_result)
            if login_screenshot_path:  
                await send_error(channel, login_screenshot_path)

        google_result, google_screenshot_path = await run_test(test_google_button)
        if "Google button works well" not in google_result:
            await channel.send(google_result)
            if google_screenshot_path:  
                await send_error(channel, google_screenshot_path)

        email_result, email_screenshot_path = await run_test(selenium_test_email)
        if "Email button works well" not in email_result:
            await channel.send(email_result)
            if email_screenshot_path:  
                await send_error(channel, email_screenshot_path)

        demo_result, demo_screenshot_path = await run_test(selenium_test_demo_button)
        if "Demo, mic and camera buttons are works well" not in demo_result:
            await channel.send(demo_result)
            if demo_screenshot_path:  
                await send_error(channel, demo_screenshot_path)


if __name__ == "__main__":
    bot.run(BOT_TOKEN)

