from selenium import webdriver
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from datetime import datetime
import time
import os
import sys
import argparse

def construct_topic_url(topic):
	"""
	Helper function to construct url for the topic given.
	"""
	return 'https://www.quora.com/topic/' + topic + '/all_questions'

def write_now(file_question_urls, file_questions, starting_point, browser):
	"""
	Helper function to write questions and their URLs to specific files mentioned
	Also starting_point decides the starting index of the questions that need to
	be written
	"""
	html_source = browser.page_source
	data = html_source.encode('utf-8')
	soup = BeautifulSoup(data)

	mydivs = soup.findAll("a", { "class" : "question_link" })
	for index, div in enumerate(mydivs):
		if starting_point <= index:
			file_question_urls.write(div['href'].encode('utf-8') + "\n")
			print div['href']
			file_questions.write(div.findAll("span", { "class" : "rendered_qtext" })[0].text.encode('utf-8') + "\n")

	file_question_urls.close()
	file_questions.close()

def get_topic_questions(topic, num_posts, driver_location):
	"""
	Gets list of questions for the topic until required limit is reached.
	"""
	file_question_urls =  open(topic + "small_question_urls.txt", mode = 'ab')
	file_questions =  open(topic + "small_questions.txt", mode = 'ab')
	if not os.path.isfile(topic + "_scrolls"):
		open(topic + "_scrolls", 'a').close()
	topic_scrolls = open(topic + "_scrolls", mode = 'rb+')
	counts = topic_scrolls.readlines()

	if len(counts) < 1:
		starting_point = 0
	else:
		starting_point = int(counts[-1][:-1])

	current_url = construct_topic_url(topic)
	print 'Starting from %d' % (starting_point)
	#display = Display(visible=0, size=(800, 600))
	#display.start()
	browser = webdriver.Chrome(driver_location)
	browser.get(current_url)

	print browser.title
	posts = browser.find_elements_by_css_selector("div.pagedlist_item")
	prev_len = 0
	current_post_len = len(posts)
	counter = 0

	while len(posts) < num_posts:
		#browser.execute_script("arguments[0].scrollIntoView();", posts[-1])
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight * 10)")
		posts = browser.find_elements_by_css_selector("div.pagedlist_item")
		time.sleep(3)
		print 'Scrolling for %s %d' % (topic, len(posts))
		print datetime.now()
		prev_len = current_post_len
		current_post_len = len(posts)
		if current_post_len == prev_len:
			counter = counter + 1
		else:
			counter = 0
		if counter > 15:
			print 'Please help!!!!!!!!!'
			time.sleep(60)
		if counter > 20:
			write_now(file_question_urls, file_questions, starting_point, browser)
			print 'Starting again!'
			browser.quit()
			# display.stop()
			if starting_point <= len(posts) + 20:
				topic_scrolls.write(str(len(posts)+ 20) + '\n')
				topic_scrolls.flush()
				topic_scrolls.close()
				return len(posts) + 20

	write_now(file_question_urls, file_questions, starting_point, browser)

	browser.quit()
	topic_scrolls.close()
	return len(posts)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--topic', type=str, default='Entertainment',
		help='topic name')
	parser.add_argument('--num_posts', type=int, default=400,
		help='No. of questions to be scraped')
	parser.add_argument('--driver_location', type=str,
	default='/Users/vj/quora_crawl/chromedriver',
		help='Location of your chromedriver')

	args = parser.parse_args()
	while True:
		try:
			starting_point = get_topic_questions(args.topic, args.num_posts, args.driver_location)
			if starting_point < args.num_posts:
				print 'Going again!'
				continue
		except ValueError as e:
			continue
		break

if __name__ == "__main__":
	main()
