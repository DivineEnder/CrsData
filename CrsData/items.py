# @Author: DivineEnder
# @Date:   2018-03-08 00:50:28
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2018-03-11 01:21:38

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

class Course(scrapy.Item):
	crn = scrapy.Field()
	dept = scrapy.Field()
	dept_num = scrapy.Field()
	title = scrapy.Field()
	term_year = scrapy.Field()
	crs_type = scrapy.Field()
	credits = scrapy.Field()
	status = scrapy.Field()
	mt_day = scrapy.Field()
	mt_start_time = scrapy.Field()
	mt_end_time = scrapy.Field()
	loc_building = scrapy.Field()
	loc_room = scrapy.Field()
	sec_enrolled = scrapy.Field()
	sec_enroll_cap = scrapy.Field()
	total_enrolled = scrapy.Field()
	total_enroll_cap = scrapy.Field()
	comments = scrapy.Field()
	prof = scrapy.Field()
	prereqs = scrapy.Field()
	descrip = scrapy.Field()
	url = scrapy.Field()

def parse_time(time):
	if len(time) == 3:
		return time[:1] + ':' + time[1:]
	else:
		return time[:2] + ':' + time[2:]

def parse_cap(cap):
	try:
		int(cap)
	except ValueError:
		return -1

	return cap

def parse_dept(dept_str):
	return dept_str.replace(" ", "")[:3]

def parse_dept_num(dept_str):
	return dept_str.replace(" ", "")[3:]

class CourseLoader(ItemLoader):
	default_output_processor = TakeFirst()

	crn_in = MapCompose(int)
	dept_in = MapCompose(parse_dept)
	dept_num_in = MapCompose(parse_dept_num)
	mt_start_time_in = MapCompose(parse_time)
	mt_end_time_in = MapCompose(parse_time)
	sec_enrolled_in = MapCompose(int)
	sec_enroll_cap_in = MapCompose(parse_cap, int)
	total_enrolled_in = MapCompose(int)
	total_enroll_cap_in = MapCompose(parse_cap, int)
