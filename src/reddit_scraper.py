import praw
import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf8')

data = {}

r = praw.Reddit(user_agent = "some random bullshit version 1.6577333")

num_submissions = 0
file_id = 0
for s in praw.helpers.submissions_between(r, 'bitcoin'):
	try:
		num_submissions += 1
		date_string = datetime.datetime.fromtimestamp(s.created).strftime('%m-%d-%Y')
		if(date_string not in data):
			data[date_string] = {}

		key = (str(s.title), s.score)
		data[date_string][key] = {}
		# print("-----------------------------")
		# print("Title: " + str(s.title))
		# print("Link: " + str(s.short_link))
		# print("Created at: " + str(s.created))
		# print("Comments: ")
		flat_comments = praw.helpers.flatten_tree(s.comments)
		for comment in flat_comments:
			data[date_string][key][str(comment.body)] = comment.score

		print("Num submissions processed: " + str(num_submissions))

		if(num_submissions % 100 == 0):
			f = open("./data/reddit_skeddit_backup_" + str(file_id), "w")
			file_id += 1
    		f.write(str(data))
    		f.close()
    		data = {}

	except Exception as e:
		print(e)
		continue

