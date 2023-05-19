from app.models import MailingStats


def collect_stats(data, mailing):

    stat = MailingStats.objects.create(mailing=mailing)

    count_ok = 0
    count_fail = 0

    for dt in data:
        if dt["message"] == "OK":
            count_ok += 1
        else:
            count_fail += 1

    stat.no_messages_ok = count_ok
    stat.no_message_fail = count_fail
    stat.no_messages = len(data)

    stat.save()