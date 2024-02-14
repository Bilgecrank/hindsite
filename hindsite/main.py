"""
Activation point for the application.
"""

import os

from flask_bootstrap import Bootstrap5
from hindsite import create_app

app = create_app()

bootstrap = Bootstrap5(app)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default="80"))
