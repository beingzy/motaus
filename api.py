"""
"""
import typing
import uuid

from collections import namedtuple
from numpy.testing._private.utils import IgnoreException
from pandas import DataFrame


# temporary storage object used for development purpose
URLPair = namedtuple("URLPair", ["id", "long_url", "short_url"])
URL_PAIR_STORE = DataFrame([], columns=["id", "long_url", "short_url"])
DOMAIN_NAME = "https://tiny_url.io"


def gen_shorter_url(long_url):
    """convert URL to a shorter one of a fixed length

       step01: check if the long_url has already been in the DB
    """
    if long_url in URL_PAIR_STORE.long_url:
        return URL_PAIR_STORE.short_url[
            URL_PAIR_STORE.long_url == long_url]
    else:
        short_url = DOMAIN_NAME + '/' + do_hashing(long_url)
        new_entry = URLPair(
            id=gen_unique_id(),
            long_url=long_url,
            short_url=short_url,
        )
        insert_new_pairs(new_entry)
        return short_url


def get_original_url(short_url):
    """find the origianl URL by looking up the table with
       short_url
    """
    global URL_PAIR_STORE
    record_idx = URL_PAIR_STORE.short_url == short_url
    if sum(record_idx) == 0:
        raise ValueError(f"Failed to find `{short_url}` in records!")
    else:
        return URL_PAIR_STORE.long_url[record_idx].values[0]


def do_hashing(long_url):
    """
    """
    global URL_PAIR_STORE
    SHORT_URL_LENGTH = 6
    hashed = str(uuid.uuid4())[:SHORT_URL_LENGTH]
    while (sum(URL_PAIR_STORE.short_url == hashed) > 0):
        hashed = hashed[:SHORT_URL_LENGTH-2] + str(uuid.uuid4())[:2]
    return hashed


def reverse_hashing(short_url):
    """
    """
    raise NotImplementedError


def insert_new_pairs(entry: URLPair):
    global URL_PAIR_STORE
    if ((sum(URL_PAIR_STORE.id == entry.id) > 0) or 
        (sum(URL_PAIR_STORE.long_url == entry.long_url) > 0) or
        (sum(URL_PAIR_STORE.short_url == entry.short_url) > 0)):
        raise ValueError("Record contains duplicated information already in DB")
    else:
        entry_dict = {
            "id": entry.id, 
            "long_url": entry.long_url,
            "short_url": entry.short_url}
        URL_PAIR_STORE = URL_PAIR_STORE.append(
            entry_dict, ignore_index=True)


def gen_unique_id():
    import uuid
    return str(uuid.uuid4()) 

