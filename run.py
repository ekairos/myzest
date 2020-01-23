#! usr/bin/env python3.6
# coding: utf-8

from myzest import app


if __name__ == "__main__":
    app.run(host="localhost",
            port=int("5000"),
            debug=True)
