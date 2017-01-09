#!/usr/bin/env python3

from datetime import datetime

print("""\
<html>
    <body>
        <p>%s</p>
    </body>
</html>""" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
