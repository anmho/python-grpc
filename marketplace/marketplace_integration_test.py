from urllib.request import urlopen


def test_render_homepage():
    homepage_html = urlopen("http://localhost:5000").read().decode("utf-8")

    assert "<title>Book Recommendations</title>" in homepage_html