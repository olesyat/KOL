from flask import Flask, render_template, redirect, request
from db import Neo4j_Executor
import pandas as pd
from ast import literal_eval
from wordcloud import WordCloud
import matplotlib.pyplot as plt

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

keywords = pd.read_csv('keywords-Copy1.csv')
keywords['pdf_json_files'] = keywords['pdf_json_files'].map(literal_eval)

@app.route('/')
def welcome():
    distinct_countries = "MATCH (n:Author) RETURN DISTINCT n.country"
    connection = Neo4j_Executor("bolt://127.0.0.1:7687", "neo4j", "1Ucuofficial!")
    res = sorted(connection.create_query(distinct_countries))
    connection.close()
    print(res)
    return render_template("index.html", distinct_countries=res)

@app.route('/filter_institution2/<var>')
def filter_institution2(var):
    distinct_communities = f"MATCH (n:Author) WHERE n.institution CONTAINS '{var}' RETURN distinct n.community"
    top_authors = f"MATCH (n:Author) where n.institution CONTAINS '{var}'  RETURN n.name ORDER BY n.pagerank DESC LIMIT 5"
    connection = Neo4j_Executor("bolt://127.0.0.1:7687", "neo4j", "1Ucuofficial!")
    res = connection.create_query(distinct_communities)
    communities = []
    for c in res:
        q = f"MATCH (n:Author) WHERE n.community = {c} AND n.institution CONTAINS '{var}' RETURN distinct n.name"
        communities.append([c, connection.create_query(q)])

    top_authors = connection.create_query(top_authors)
    connection.close()
    print(res)
    query = f"MATCH (n: Author)-[r:Linked]->(m: Author) WHERE n.institution CONTAINS '{var}' RETURN *"
    query_dict = {"test": query}
    print(query)
    return render_template('filter_institution2.html', query_dict=query_dict, institution=var, authors=communities, top_authors=top_authors)


@app.route('/filter_country2/<var>')
def filter_country2(var):
    distinct_universities = f"MATCH (n:Author) WHERE n.country = '{var}' RETURN distinct n.institution AS institution"
    top_authors = f"MATCH (n:Author) where n.country='{var}' RETURN n.name ORDER BY n.pagerank DESC LIMIT 5"
    connection = Neo4j_Executor("bolt://127.0.0.1:7687", "neo4j", "1Ucuofficial!")
    res = connection.create_query(distinct_universities)
    authors = sorted(connection.create_query(top_authors))
    res = [uni.split('|') for uni in res if uni]
    res = sorted(list({item for sublist in res for item in sublist}))
    # for i in range(len(res)):
    #     query_count = f"MATCH (n:Author) WHERE n.institution contains '{res[i]}' RETURN count(distinct n.name)"
    #     count = connection.create_query(query_count)[0]
    #     if count < 5:
    #         del res[i]
    connection.close()
    query = f"MATCH (n: Author)-[r:Linked]->(m: Author) WHERE n.country = '{var}' RETURN *"
    query_dict = {"test": query}
    return render_template('filter_country2.html', query_dict=query_dict, institution=res, country=var, authors=authors)

@app.route('/filter_author/<var>/<uni>')
def filter_author(var, uni):
    print(uni)
    var2 = literal_eval(var)[1]
    words = ''.join(keywords[keywords.name_spelling.isin(var2)].keywords.values)

    wordcloud = WordCloud(width=800, height=550,
                          background_color='white',
                          min_font_size=10, collocations=False).generate(words)

    wordcloud.to_file('static/new_plot.png')
    return render_template('wordcloud.html', name='new_plot', url='/static/new_plot.png', var=literal_eval(var), uni=uni)

if __name__ == '__main__':
    app.run()
