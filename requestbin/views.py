import urllib
from flask import session, redirect, url_for, escape, request, render_template, make_response
import jwt

from requestbin import app, bp, db

def update_recent_bins(name):
    if 'recent' not in session:
        session['recent'] = []
    if name in session['recent']:
        session['recent'].remove(name)
    session['recent'].insert(0, name)
    if len(session['recent']) > 10:
        session['recent'] = session['recent'][:10]
    session.modified = True


def expand_recent_bins():
    if 'recent' not in session:
        session['recent'] = []
    recent = []
    for name in session['recent']:
        try:
            recent.append(db.lookup_bin(name))
        except KeyError:
            session['recent'].remove(name)
            session.modified = True
    return recent

@bp.route('/')
def home():
    try:
        if(app.config.AUTH_COOKIE_NAME):
            # If there is a cookie defined, then access to the index
            # requires authentication via a signed JWT
            authcookie = request.cookies.get(app.config.AUTH_COOKIE_NAME)
            jwt.decode(authcookie, app.config.AUTH_SECRET)
            
        # If the JWT decodes, then it is valid, so we can render the index page
        return render_template('home.html', recent=expand_recent_bins())
    except:
        # Failed cookie check so force user to re-auth.
        # TODO: handle rendering exceptions separately
        return redirect(app.config.AUTH_REDIRECT)


@bp.route('/<name>', methods=['GET', 'POST', 'DELETE', 'PUT', 'OPTIONS', 'HEAD', 'PATCH', 'TRACE'])
def bin(name):
    try:
        bin = db.lookup_bin(name)
    except KeyError:
        return "Not found\n", 404
    if request.query_string == 'inspect':
        if bin.private and session.get(bin.name) != bin.secret_key:
            return "Private bin\n", 403
        update_recent_bins(name)
        # Generate an externally valid URL
        exturl = url_for('.bin', name=name, _external=True, _scheme=app.config.PREFERRED_URL_SCHEME)
        return render_template('bin.html',
                               bin=bin,
                               exturl=exturl
        )
    else:
        db.create_request(bin, request)
        resp = make_response("ok\n")
        return resp


@bp.route('/docs/<name>')
def docs(name):
    doc = db.lookup_doc(name)
    if doc:
        return render_template('doc.html',
                               content=doc['content'],
                               title=doc['title'],
                               recent=expand_recent_bins()
        )
    else:
        return "Not found", 404
