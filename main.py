from flask import Flask, render_template, request, jsonify
from search import perform_search, perform_pagerank

app = Flask(__name__)


@app.route("/")
def test():
	return render_template('index.html')


@app.route("/search", methods=["POST"])
def search():
	query = request.form['query']
	ordering = request.form.get('ordering', 'relevance')
	rank_by = request.form.get('rank_by', 'pyscore')

	if rank_by == 'pyscore':
		search_results = perform_search(query, ordering)
	elif rank_by == 'pagerank':
		search_results = perform_pagerank(query, ordering)

	return jsonify(search_results)


if __name__ == '__main__':
	app.run(debug=True)
