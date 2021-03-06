import re
from server import app, socketio
from sql.methods import add_url, get_urls, get_tracker_data, track_user
from flask import request, render_template, redirect


@app.route("/", methods=["POST", "GET"])
def create_url():
    if request.method == 'GET':
        return render_template('main.html')

    url = request.values.get('url')

    pattern = r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'

    if not re.match(pattern, url):
        return 'Invalid URL'

    if 'www' not in url:
        url = f'www.{url}'

    if 'https://' not in url:
        url = f'https://{url}'

    tracker_url = add_url(url)

    return redirect(f'/tracker/{tracker_url}/')


@app.route("/<shortened_url>/", methods=["GET"])
def redirect_to_url(shortened_url):
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    tracker_data = track_user(shortened_url, user_ip=ip, user_agent=user_agent)

    urls = get_urls(shortened_url)

    if urls is None:
        return render_template('404.html')

    socketio.emit('tracker_data', tracker_data, to=urls['tracker_url'])

    return redirect(urls['url'])


@app.route("/tracker/<tracker_url>/", methods=["GET"])
def tracker(tracker_url):
    tracker_data = get_tracker_data(tracker_url)

    if tracker_data is None:
        return render_template('404.html')

    domain = request.url_root
    tracker_data['domain'] = domain
    return render_template('tracker.html', context=tracker_data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
