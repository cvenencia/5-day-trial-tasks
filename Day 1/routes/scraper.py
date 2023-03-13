from flask import render_template, request, session

from app import app, sock


@app.route('/scraper')
def scrape():
    try:
        session['urls'] = request.args.get('urls')
    except:
        session['urls'] = None

    from scraper.scraper import scrape_pages
    results = scrape_pages(**session)

    return render_template('scraper.html', title="asdf", results=results)
