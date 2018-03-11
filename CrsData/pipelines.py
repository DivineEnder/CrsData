# @Author: DivineEnder
# @Date:   2018-03-08 22:24:45
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2018-03-11 01:25:41

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from dotenv import load_dotenv, find_dotenv
from Utils import connection_utils as glc

from psycopg2.extensions import AsIs

import os

class CrsdataPipeline(object):

	def open_spider(self, spider):
		# Load the environment file
		# This load makes sure passwords are not stored on github
		# Basically here for security reasons
		load_dotenv(find_dotenv())
		# Generate a new database connection (will default to credentials loaded from the env file)
		self.connection = glc.open_new_connection(host = os.environ.get("DBHOST"), port = os.environ.get("DBPORT"), user = os.environ.get("DBUSER"), password = os.environ.get("DBPASS"), dbname = os.environ.get("DBNAME"))
		# Generate a new cursor from the previously generated connection
		self.cursor = glc.open_new_cursor(self.connection)

	def process_item(self, course, spider):
		# input() # <---- Debugging print (the god)
		# Insert course into database
		self.cursor.execute("""INSERT INTO courses (%s) VALUES %s ON CONFLICT (crn) DO NOTHING""",(
			AsIs(','.join(course.keys())),
			tuple([course[field] for field in course.keys()])
		))
		# Commit all changes to the database
		self.connection.commit()

		return course

	def close_spider(self, spider):
		# Close DB connection and cursor
		glc.close_cursor(self.cursor)
		glc.close_connection(self.connection)
