from fetch_mails import fetch_google_alerts
from generate_digest import generate_digest
from parse_mail import parse_mail
from score_with_llm import score_paper
from send_mail import send_scholar_rapport_by_mail
from utils.logger import setup_logger


def main():
    logger = setup_logger()
    logger.info("Starting...")
    mails = fetch_google_alerts()
    if not mails:
        logger.info("No new mails found, exit.")
        return

    scored = []
    for mail in mails:
        items = parse_mail(mail["html"])
        for item in items:
            score = score_paper(title=item["title"], abstract=item["abstract"])
            scored.append({**item, **score})

    digest, n_items = generate_digest(scored)
    if n_items == 0:
        logger.info("No relevant items found, exit.")
        return

    with open("digest.md", "w") as f:
        f.write(digest)

    send_scholar_rapport_by_mail(digest)


if __name__ == "__main__":
    main()
