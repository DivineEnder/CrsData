# @Author: DivineEnder
# @Date:   2018-03-08 00:51:32
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2018-03-08 11:57:39


# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from CrsData.items import Course
from CrsData.items import CourseLoader


class CdcsSpider(scrapy.Spider):
	name = 'cdcs'
	start_urls = ['https://cdcs.ur.rochester.edu//']

	def parse(self, response):
		yield scrapy.FormRequest.from_response(response = response, formdata = {
			'ddlTerm': 'D-20191',
			'txtCourse': 'PHY'
		}, callback = self.parse_results)

	def build_course_loader(self, selector, xpaths):
		# Create the item loader for creating items
		loader = CourseLoader(item = Course(), selector = selector) # <----- THIS IS THE BULLSHIT, the RESULT IS USING THE PARENT TABLE/ SELECTORLIST WHICH CAUSES THE PATHS TO FIND ALL TABLES INSTEAD OF JUST ONE

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
			loader.add_value("course_type", "main")
		# If the credits are not floats...
		except ValueError:
			# The course type is specified in the credits cell previously parsed
			loader.add_value("course_type", credits)

		return loader

	def parse_results(self, response):
		# Get all the course tables
		results = response.xpath("//table[@width='100%'][@cellspacing='0'][@cellpadding='3'][@border='0']")
		# Generate all the xpaths for the various course fields
		paths_dict = {
			"CRN": "tr/td/span[contains(@id, 'CRN')]/text()",
			"dept": "tr/td/span[contains(@id, 'CNum')]/text()",
			"dept_num": "tr/td/span[contains(@id, 'CNum')]/text()",
			"title": "tr/td[contains(@id, 'Title')]/span/text()",
			"term": "tr/td[contains(@id, 'Term')]/span/text()",
			"status": "tr/td[contains(@id, 'Credits')]/span/text()",
			"mt_day": "tr/td/table/tr/td/span[contains(@id, 'Day')]/text()",
			"mt_start_time": "tr/td/table/tr/td/span[contains(@id, 'StartTime')]/text()",
			"mt_end_time": "tr/td/table/tr/td/span[contains(@id, 'EndTime')]/text()",
			"loc_building": "tr/td/table/tr/td/span[contains(@id, 'Building')]/text()",
			"loc_room": "tr/td/table/tr/td/span[contains(@id, 'Room')]/text()",
			"sec_enrolled": "tr/td/span[contains(@id, 'SectionEnroll')]/text()",
			"sec_enroll_cap": "tr/td/span[contains(@id, 'SectionCap')]/text()",
			"total_enrolled": "tr/td/span[contains(@id, 'TotEnroll')]",
			"total_entroll_cap": "tr/td/span[contains(@id, 'TotalCap')]",
			"comments": "tr/td/span[contains(@id, 'Comments')]/text()",
			"prof": "tr/td/span[contains(@id, 'Instructors')]/text()",
			"prereqs": "tr/td/span[contains(@id, 'Prerequisites')]/text()",
			"desc": "tr/td/span[contains(@id, 'Desc')]/text()"
		}

		for result in results:
			courses = []

			loader = self.build_course_loader(result, paths_dict)
			courses.append(loader.load_item())
			print(courses)
			input()

		return courses
