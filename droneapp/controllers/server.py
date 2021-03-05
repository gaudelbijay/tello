import logging
import config

logger = logging.getLogger(__name__)
app = config.app


@app.route('/')
def index():
    return "hello world!"


