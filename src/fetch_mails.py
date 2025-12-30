from email import message_from_bytes, policy
from logging import getLogger

from imapclient import IMAPClient

from config import EMAIL_ADDRESS, EMAIL_PASSWORD, IMAP_HOST, IMAP_PORT


def fetch_google_alerts():
    logger = getLogger(__name__)
    logger.info("Fetching Google Alerts from IMAP server")
    mails = []
    with IMAPClient(IMAP_HOST, port=IMAP_PORT, ssl=True) as server:
        logger.info("Logging in to IMAP server")
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.select_folder("Papers")
        uids = server.search(["UNSEEN"])
        logger.info(f"Fetched {len(uids)} unseen mails")
        fetch_map = server.fetch(uids, ["BODY[]", "ENVELOPE"])
        for uid, data in fetch_map.items():
            msg = message_from_bytes(data[b"BODY[]"], policy=policy.default)
            logger.info(f"Fetch mail UID {uid} with subject: {msg.get('subject')}, from {msg.get('from')}")
            mails.append({
                "uid": uid,
                "subject": msg.get("subject"),
                "html": msg.get_content(),
            })
    return mails
