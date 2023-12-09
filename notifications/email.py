import os
from dotenv import load_dotenv
import datetime
import resend

from crawlers.crawler import FlatResult

load_dotenv()
resend.api_key = os.environ["RESEND_API_KEY"]


def send_email(to: str, results: list[FlatResult]):
    today = datetime.date.today()

    body = ""
    for result in results:
        body += f"<p><a href='{result['url']}'>{result['title']}</a><img src='{result["images"][0] if result["images"] else ""}'/></p>"

    resend.Emails.send(
        {
            "from": "Flat Digest <flats@updates.joshuaknauber.com>",
            "to": to,
            "subject": f"Flat Digest for {today.strftime("%d.%m.%Y")}",
            "html": "<p>Here are the flats for today:</p>" + body,
        }
    )
