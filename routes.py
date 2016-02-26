#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.handlers import *

#This is the place where all of your URL mapping goes
route_list = [
	(r'^/', MainHandler),
	(r'^/photos',PhotoHandler),
	(r'^/photos/(\w+)',CollectionHandler),
	(r'^/admin',AdminHandler),
	(r'^/list',VideoLister),
	(r'^/delete',DeleteHandler),
	(r'^/dropdb/(\w+)',DropHandler),
	(r'^/signin',SigninHandler),
	(r'^/seed',SeedHandler),
	(r'^/useradd',AddUsers),
	(r'^/debug',DebugHandler),
	(r'^/askyoutube',YouTubeRequest)
	]
