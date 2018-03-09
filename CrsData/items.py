# @Author: DivineEnder
# @Date:   2018-03-08 00:50:28
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2018-03-08 12:04:01

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, TakeLast

class Course(scrapy.Item):
	CRN = scrapy.Field(serializer = int)
	dept = scrapy.Field()
	dept_num = scrapy.Field()
	title = scrapy.Field()
	term = scrapy.Field()
	course_type = scrapy.Field()
	credits = scrapy.Field(serializer = float)
	status = scrapy.Field()
	mt_day = scrapy.Field()
	mt_start_time = scrapy.Field(serializer = int)
	mt_end_time = scrapy.Field(serializer = int)
	loc_building = scrapy.Field()
	loc_room = scrapy.Field(serializer = int)
	sec_enrolled = scrapy.Field(serializer = int)
	sec_enroll_cap = scrapy.Field(serializer = int)
	total_enrolled = scrapy.Field(serializer = int)
	total_entroll_cap = scrapy.Field(serializer = int)
	comments = scrapy.Field()
	prof = scrapy.Field()
	prereqs = scrapy.Field()
	desc = scrapy.Field()
	url = scrapy.Field()

class CourseLoader(ItemLoader):
	default_output_processor = TakeFirst()

	CRN_in = MapCompose(int)
	dept_in = MapCompose()



	def parse_dept(data):


	# name_in = MapCompose(unicode.title)
	# name_out = Join()
	#
	# price_in = MapCompose(unicode.strip)
