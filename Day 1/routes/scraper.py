from flask import render_template, request, session

from app import app, sock


@app.route('/scraper')
def scrape():
    try:
        session['urls'] = request.args.get('urls')
    except:
        session['urls'] = None

    return render_template('scraper.html', title="Results")


@sock.route('/connect')
def handle_message(socket):
    def log(message, end='\n', tab=0):
        tabulation = '    '
        socket.send(f'{tabulation * tab}{message}{end}')

    from scraper.scraper import scrape_pages
    scrape_pages(log, **session)
    socket.close()
