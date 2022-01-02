import re
from server import app
from sql.methods import add_url, get_url, get_tracker_data, track_user
from flask import request, render_template, redirect


@app.route("/", methods=["POST", "GET"])
def create_url():
    if request.method == 'GET':
        return render_template('create.html')

    url = request.values.get('url')

    pattern = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'

    if not re.match(pattern, url):
        return 'Invalid URL'

    tracker_url = add_url(url)

    return redirect(f'/tracker/{tracker_url}/')


@app.route("/<shortened_url>/", methods=["GET"])
def redirect_to_url(shortened_url):
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    track_user(shortened_url, user_ip=ip, user_agent=user_agent)
    url = get_url(shortened_url)

    if url is None:
        return render_template('404.html')

    return redirect(url)


@app.route("/tracker/<tracker_url>/", methods=["GET"])
def tracker(tracker_url):
    tracker_data = get_tracker_data(tracker_url)

    if tracker_data is None:
        return render_template('404.html')

    domain = request.url_root
    tracker_data['domain'] = domain
    return render_template('tracker.html', context=tracker_data)
