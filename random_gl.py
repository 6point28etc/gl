import os
import sys
import random
import wikipedia
from wikipedia import RedirectError, DisambiguationError
from wsgiref.simple_server import make_server
from io import StringIO
import warnings
from bs4 import GuessedAtParserWarning
warnings.filterwarnings('ignore', category=GuessedAtParserWarning)

def random_gl (environ=None, start_response=None):
    stdout = StringIO()
    # whatever it's a small enough file and I'm lazy
    title = random.choice(open(os.path.join(os.path.dirname(sys.argv[0]), "filtered_titles.txt"), encoding="UTF-8").readlines()).strip()
    try:
        try:
            print(wikipedia.summary(title, sentences=1, redirect=False, auto_suggest=False),
                    wikipedia.page(title=title, redirect=False, auto_suggest=False).url, file=stdout)
        except RedirectError:
            print(f"(Redirected from {title.replace('_', ' ')}): ", end='', file=stdout)
            page = wikipedia.page(title=title, redirect=True, auto_suggest=False)
            print(wikipedia.summary(page.title, sentences=1, redirect=False, auto_suggest=False),
                    page.url, file=stdout)
    except DisambiguationError as e:
        print(e, file=stdout)
        print(e.url, file=stdout)   # kinda don't like this
    if start_response:
        start_response("200 OK", [('Content-Type','text/plain; charset=utf-8'), ("Access-Control-Allow-Origin", "*")])
        return [stdout.getvalue().encode("utf-8")]
    else:
        return stdout.getvalue()

if __name__ == '__main__':
    if "--server" in sys.argv:
        port = int(os.environ['PORT']) if 'PORT' in os.environ else 8000
        with make_server('', port, random_gl) as httpd:
            print(f"Serving HTTP on port {port}...")

            # Respond to requests until process is killed
            httpd.serve_forever()
    else:
        print(random_gl())
