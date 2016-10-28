# vim: set fileencoding=utf-8 :
import re


def regex_account_twitter(account):
    match = re.match(r"^(?:https?://)?(?:www.)?(?:twitter[.]com/)?(?<=^|(?<=[^a-zA-Z0-9-_\.]))@?([A-Za-z0-9_]+)/?$",
                        account.strip())
    if match:
        return match.group(1)


def regex_url_facebook(url_facebook):
    match = re.match(
        r"^(?:(?:https?://)(?:www.)?(?:facebook[.]com/)|(?:www.)?(?:facebook[.]com/))?[\/#!]*"
        r"((?:pages/[\w.\-]+\/\d+)|[\w.\-]+)\/?(?:[?].*)?$",
        url_facebook.strip())
    if match:
        return match.group(1)
