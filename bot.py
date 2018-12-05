#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import json
import datetime
import urllib
import mattermost_bridge
import requests

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class Rand(tornado.web.RequestHandler):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def prepare(self):
        pass

    def post(self):
        data = str(self.request.body).split("&")
        channel_id = data[0].split("=")[1]
        command = urllib.unquote(data[2]).decode('utf8')
        response_url = urllib.unquote(data[3].split("=")[1]).decode('utf8')
        text = urllib.unquote(data[6].split("=")[1]).decode('utf8')
        response = dict()
        response['response_type'] = "in_channel"
        headers = mattermost_bridge.headers
        headers['Content-Type'] = 'application/json'
        if len(text) == 0:
            print "random user"
            username = mattermost_bridge.get_username_by_id(mattermost_bridge.get_random_channel_member(channel_id))
            response['text'] = "The boy has chosen @%s" % username
            req = requests.post("%s" % response_url, data = json.dumps(response), headers = headers)
        else:
            print "random number"
            try:
                if len(text.spit("+")) == 2:
                    f  = int(u"%s" % text.split("+")[0])
                    to = int(u"%s" % text.split("+")[1])
                    number = mattermost_bridge.get_random_number(f, to)
                    response['text'] = "The boy has chosen %d" % number
            except:
                response['text'] = "The boy hasn't chosen anything, please send correct request"
            req = requests.post("%s" % response_url, data=json.dumps(response), headers=headers)
        print req.text

def make_app():
    application = tornado.web.Application(
        [
            (r"/test", MainHandler),
            (r"/rand", Rand),
        ]
    )
    return application

if __name__ == "__main__":
    app = make_app()
    app.listen(8800)
    print "start mattermost bridge...."
    tornado.ioloop.IOLoop.current().start()