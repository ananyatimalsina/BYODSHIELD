from dotenv import load_dotenv
load_dotenv()

from os import getenv
from datetime import datetime, timedelta

from pyunifi.controller import Controller
import webuntis

from apscheduler.schedulers.background import BackgroundScheduler
import asyncio, ssl, json
import websockets

# WebUntis setup, uncomment if needed
# untis = webuntis.Session(
#     username=getenv('UNTIS_USERNAME'),
#     password=getenv('UNTIS_PASSWORD'),
#     server=getenv('UNTIS_HOST'),
#     school=getenv('UNTIS_SCHOOL'),
#     useragent='BYODSHIELD'
# ).login()

unifi = Controller(
    host=getenv('UNIFI_HOST'),
    username=getenv('UNIFI_USERNAME'),
    password=getenv('UNIFI_PASSWORD'),
    site_id=getenv('UNIFI_SITE'),
    ssl_verify=getenv('UNIFI_SSL_VERIFY').lower() == 'true',
    port=int(getenv('UNIFI_PORT')),)

sched = BackgroundScheduler()
sched.start()

def handle_unifi_disconnect(user):
    """
    This function is called when a user disconnects from the Unifi network.
    It can be used to trigger any action, such as sending a notification or logging the event.
    """
    # Here you can implement the logic to handle the disconnection event
    print(f"User {user} has disconnected from the Unifi network.")

    # Example: Remove the user from the network
    unifi.delete_radius_user(user)

async def _listen():
    # Connect to the events WebSocket
    uri = f"wss://{getenv("UNIFI_HOST")}:8443/wss/s/{getenv("UNIFI_SITE")}/events"
    ssl_ctx = ssl._create_unverified_context()
    headers = {"Cookie": f"unifises={unifi.session.cookies.get('unifises')}"}

    async with websockets.connect(uri, ssl=ssl_ctx, additional_headers=headers) as ws:
        async for msg in ws:
            data = json.loads(msg)
            if data.get("event") == "wu.disconnected":
                user = data.get("user") or data.get("mac")
                # Trigger Flask endpoint logic
                handle_unifi_disconnect(user)

def start_unifi_listener():
    asyncio.run(_listen())

def validate_connection(user):
    """
    Query UniFi REST API to see if `user` is currently connected.
    """

    if any(c.get("user") == user for c in unifi.get_clients()):
        print(f"[OK] {user} is connected")
    else:
        print(f"[ALERT] {user} is NOT connected")
        # e.g., increment strike count or take action
        # Example: Remove the user from the network
        unifi.delete_radius_user(user)

def schedule_validation(user, delay_minutes=10):
    job_id = f"validate_{user}"
    # Remove existing job if any
    if sched.get_job(job_id):
        sched.remove_job(job_id)
        print(f"Removed existing job: {job_id}")
    
    run_date = datetime.now() + timedelta(seconds=delay_minutes)

    # Schedule new job
    sched.add_job(
        func=validate_connection,
        args=[user],
        id=job_id,
        replace_existing=True,
        trigger="date",
        run_date=run_date,
    )

    print(f"Scheduled validation for {user} in {delay_minutes} minutes")