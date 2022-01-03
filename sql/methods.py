from . import cursor
import uuid


def add_url(url):
    shortened_url = str(uuid.uuid4()).replace('-', '').upper()[:8]
    tracker_url = str(uuid.uuid4()).replace('-', '').upper()[:8]

    sql = """
        INSERT INTO url (shortened_url, tracker_url, url)
        VALUES (?, ?, ?)
    """

    cursor.execute(sql, (shortened_url, tracker_url, url))
    cursor.connection.commit()
    return tracker_url


def get_urls(shortened_url):
    sql = """
        SELECT url, shortened_url, tracker_url FROM url WHERE shortened_url = ?
    """
    cursor.execute(sql, (shortened_url,))

    res = cursor.fetchone()

    if res is None:
        return None

    return res


def get_tracker_data(tracker_url):
    sql = """
        SELECT * FROM url WHERE tracker_url = ?
    """

    cursor.execute(sql, (tracker_url,))

    tracker_data = cursor.fetchone()

    if tracker_data is None:
        return None

    sql = """
        SELECT * FROM visit WHERE url_id = ?
    """

    cursor.execute(sql, (tracker_data.get('url_id'),))
    visits = cursor.fetchall()

    tracker_data['visits'] = visits

    return tracker_data


def track_user(shortened_url, user_ip, user_agent):
    sql = """
        SELECT url_id FROM url WHERE shortened_url = ?
    """

    cursor.execute(sql, (shortened_url,))

    res = cursor.fetchone()

    if res is None:
        return

    url_id = res.get('url_id')

    sql = """
        INSERT INTO visit (url_id, ip, user_agent)
        VALUES (?, ?, ?)
    """

    cursor.execute(sql, (url_id, user_ip, user_agent))
    cursor.connection.commit()

    visit_id = cursor.lastrowid

    sql = """
        SELECT ip, user_agent, created_at FROM visit WHERE visit_id = ?
    """

    cursor.execute(sql, (visit_id,))
    visit = cursor.fetchone()

    return visit
