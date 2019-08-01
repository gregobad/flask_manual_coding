import csv
from flask import Flask
from flask import request, render_template, redirect, url_for

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

app = Flask(__name__)

transcripts = {}
coder_counts = {}

with open('/home/greg/research/localnews/mturk_sample.csv', 'r') as csvfile:
	transcriptreader = csv.DictReader(csvfile)
	for row in transcriptreader:
		key = ','.join([row['station_id'],row['date'],row['time_seq'],row['timeblock_ampm']])
		transcript = row['transcript'].encode('ascii', 'ignore')
		transcripts[key] = transcript


classwriter = csv.writer(open('/home/greg/research/localnews/classifications.csv', 'a'))

@app.route('/classify', methods = ['GET'])
def classify():
	label = request.args.get('category', '')
	coder = request.args.get('coder', '')
	key = request.args.get('key', '')

	if coder == '':
		coder = 'Your Name Here'
		count = 1
	else:
		coder_counts[coder] = coder_counts.get(coder, 0) + 1
		count = coder_counts[coder]
	

	if request.args.get('again', '') == "done":
		return redirect(url_for('alldone', count = count))

	if label != '':
		classwriter.writerow([key, coder, label])

	(k,v) = transcripts.popitem()
	return render_template('classifier.html', key=k, transcript=v, name = coder, count = count)

@app.route('/alldone/<count>')
def alldone(count):
	return render_template('thanks.html', count = count)