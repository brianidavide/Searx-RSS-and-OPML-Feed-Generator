from flask import Flask, send_file
import searx_rss_generator

app = Flask(__name__)

@app.route('/rss')
def serve_rss():
    searx_rss_generator.generate_rss_feed()
    return send_file("searx_rss_feed.xml", mimetype="application/rss+xml")

if __name__ == "__main__":
    app.run(port=8000)
