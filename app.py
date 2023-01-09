from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_score.pkl','rb'))
final = pickle.load(open('final.pkl','rb'))
cosine_pairwise_df = pickle.load(open('cosine_df.pkl','rb'))
cosine_pairwise = pickle.load(open('cosine.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_rating'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    global result
    user_input = request.form.get('user_input')
    temp = list(cosine_pairwise_df.sort_values([user_input], ascending=True).head(10).index)
    book_list = []
    data = []
    for i in temp:
        book_list = book_list + list(final[final['User_ID'] == i]['Book_Title'])
        result = set(book_list) - set(final[final['User_ID'] == user_input]['Book_Title'])
        result = list(result)[:8]
    for i in result:
        item = []
        temp_df = books[books['Book-Title'] == i]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)


    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)