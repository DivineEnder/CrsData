# @Author: DivineEnder
# @Date:   2018-03-08 00:51:32
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2018-03-11 01:33:27


# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from CrsData.items import Course
from CrsData.items import CourseLoader

import Utils.common_utils as utils

class CdcsSpider(scrapy.Spider):
	name = 'cdcs'
	start_urls = ['https://cdcs.ur.rochester.edu//']

	def parse(self, response):
		yield scrapy.FormRequest.from_response(response = response, formdata = {
			'ddlTerm': 'D-20191', # Fall 2018 :: D-20191 # Spring 2018 :: D-20182
			'txtCourse': 'EES'
		}, callback = self.parse_results)

	def build_course_loader(self, selector, xpaths):
		# Create the item loader for creating items
		loader = CourseLoader(item = Course(), selector = selector)

		# Parse the fields using the given xpaths
		for field, path in xpaths.items():
			loader.add_xpath(field, path)

		# Parse credits
		credits = selector.xpath("tr/td/span[contains(@id, 'Credits')]/text()").extract_first().replace(" ", "")
		# Check if credits are floats
		try:
			credits = float(credits)
			# If so load the credits
			loader.add_value("credits", credits)
			# The course is a main course (i.e. not recitation, workshop, etc.)
			loader.add_value("crs_type", "MAIN")
		# If the credits are not floats...
		except ValueError:
			# The course type is specified in the credits cell previously parsed
			loader.add_value("crs_type", credits)

		return loader

	def build_course(self, result, paths_dict):
		loader = self.build_course_loader(result, paths_dict)
		course = loader.load_item()
		return course

	def parse_results(self, response):
		# Get all the course tables
		results = response.xpath("//table[@width='100%'][@cellspacing='0'][@cellpadding='3'][@border='0']")
		# Generate all the xpaths for the various course fields
		paths_dict = {
			"crn": "tr/td/span[contains(@id, 'CRN')]/text()",
			"dept": "tr/td/span[contains(@id, 'CNum')]/text()",
			"dept_num": "tr/td/span[contains(@id, 'CNum')]/text()",
			"title": "tr/td/span[contains(@id, 'Title')]/text()",
			"term_year": "tr/td/span[contains(@id, 'Term')]/text()",
			"status": "tr/td/span[contains(@id, 'Status')]/text()",
			"mt_day": "tr/td/table/tr/td/span[contains(@id, 'Day')]/text()",
			"mt_start_time": "tr/td/table/tr/td/span[contains(@id, 'StartTime')]/text()",
			"mt_end_time": "tr/td/table/tr/td/span[contains(@id, 'EndTime')]/text()",
			"loc_building": "tr/td/table/tr/td/span[contains(@id, 'Building')]/text()",
			"loc_room": "tr/td/table/tr/td/span[contains(@id, 'Room')]/text()",
			"sec_enrolled": "tr/td/span[contains(@id, 'SectionEnroll')]/text()",
			"sec_enroll_cap": "tr/td/span[contains(@id, 'SectionCap')]/text()",
			"total_enrolled": "tr/td/span[contains(@id, 'TotEnroll')]/text()",
			"total_enroll_cap": "tr/td/span[contains(@id, 'TotalCap')]/text()",
			"comments": "tr/td/span[contains(@id, 'Comments')]/text()",
			"prof": "tr/td/span[contains(@id, 'Instructors')]/text()",
			"prereqs": "tr/td/span[contains(@id, 'Prerequisites')]/text()",
			"descrip": "tr/td/span[contains(@id, 'Desc')]/text()",
			"url": "tr/td/span[contains(@id, 'URL')]/a/text()"
		}

		courses = utils.return_loop_display_progress(results, self.build_course, paths_dict)

		return courses
