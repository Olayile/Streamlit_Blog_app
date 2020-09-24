import streamlit as st
import sqlite3




# #### #   ## Database
con = sqlite3.connect('database.db')
c = con.cursor()

# functions
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS reviewtable(writer TEXT, title TEXT, book TEXT, author TEXT, article TEXT, date DATE)')

def add_data(writer, title, book, author, article, date):
    c.execute('INSERT INTO reviewtable(writer, title, book, author, article, date) VALUES (?,?,?,?,?,?)',(writer, title, book, author, article, date))
    con.commit()

def view_all_reviews():
    c.execute('SELECT * FROM reviewtable')
    data = c.fetchall()
    return data

def view_all_titles():
    c.execute('SELECT DISTINCT title FROM reviewtable')
    data = c.fetchall()
    return data

def get_review_by_title(title):
    c.execute('SELECT * FROM reviewtable WHERE title="{}"'.format(title))
    data = c.fetchall()
    return data

def get_search(category, term):
    c.execute('SELECT * FROM reviewtable WHERE "{}" LIKE "%{}%"'.format(category, term))
    data = c.fetchall()
    return data

# Layout template

title_template= """
<div style= "background-color:#F0F0F0; border-radius:30px; padding:10px,margin:10px;">
<h4 style="color:black; text-align:center; ">{}</h4>
<h4 style="margin: 1em 0 0.5em 0;
	font-weight: 600;
	font-family: 'Titillium Web', sans-serif;
	position: relative;
	text-shadow: 0 -1px 1px rgba(0,0,0,0.4);
	font-size: 22px;
	line-height: 40px;
	color: #355681;
    text-align: center;
	text-transform: uppercase;
	border-bottom: 1px solid rgba(53,86,129, 0.3); ">{}</h4>
<h4 style="color:black; text-align:center; ">Book Title:{}</h4>
<h4 style="color:black; text-align:center; ">Author:{}</h4>
<h4 style=" display: block;
    width: 170px;
    height: 50px;
    background: #4E9CAF;
    padding: 10px;
    text-align: center;
    border-radius: 5px;
    color: white;
    font-weight: bold;
    line-height: 25px;">Date: {}</h4>

<p style="background-color:powderblue; text_align:center;border-radius:30px;">{}</p>

</div>



"""
selected_review_template= """
<div>
<h4 style="margin: 1em 0 0.5em 0;
	font-weight: 600;
	font-family: 'Titillium Web', sans-serif;
	position: relative;
	text-shadow: 0 -1px 1px rgba(0,0,0,0.4);
	font-size: 22px;
	line-height: 40px;
	color: #355681;
    text-align: center;
	text-transform: uppercase;
	border-bottom: 1px solid rgba(53,86,129, 0.3); ">{}</h4>
<h4 style="color:black; text-align:center; font-style: italic; ">By {}</h4>

<h4 style="color:black; text-align:center; ">Book Title: {}</h4>
<h4 style="color:black; text-align:center; ">Author: {}</h4>
<h4 style="color:black; text-align:center;">Date: {}</h4>
<p></p>
<p style="border:3px; border-style:solid; border-color:#355681; padding: 1em;">{}</p>

</div>

"""


def main():
    
    st.sidebar.image("eric-yu-artstation-small-shelf.jpg", use_column_width= True)



    st.title("Book reviews")

    menu= ["Home", "View Reviews", "Add Reviews", "Search", "Settings"]
    selected= st.sidebar.selectbox("Menu", menu)

    
    if selected == "Home":
        st.subheader("Home")

        st.image("eric_yu_composite.jpg", use_column_width= True)

        all_posts=view_all_reviews()
        for i in all_posts:
            display_writer = i[0]
            display_title = i[1]
            display_book = i[2] 
            display_author = i[3]
            display_article = str(i[4])[0:100]
            display_date = i[5]
            st.markdown(title_template.format(display_writer,display_title, display_book, display_author, display_date, display_article),  unsafe_allow_html=True)

    
    elif selected == "View Reviews":
        st.header("View Reviews")
        all_titles= [i[0] for i in view_all_titles()]
        

        post = st.sidebar.selectbox("What review would you like to see?", all_titles)

        selected_post= get_review_by_title(post)

        for i in selected_post:
            display_writer = i[0]
            display_title = i[1]
            display_book = i[2] 
            display_author = i[3]
            display_article = i[4]
            display_date = i[5]

            st.markdown(selected_review_template.format(display_title,display_writer, display_book, display_author, display_date, display_article),  unsafe_allow_html=True) #change the template





    elif selected == "Add Reviews":
        st.subheader("Add Reviews")
        create_table()

        review_writer= st.text_input("Enter Reviewer Name", max_chars=50)
        review_title= st.text_input("Enter Review Title TLDR")
        review_book= st.text_input("Enter Book Title")
        review_author= st.text_input("Enter Book author")
        review_article = st.text_area("Post Review Here", height= 200)
        review_date = st.date_input("Date")
        if st.button("ADD"):
            add_data(review_writer, review_title, review_book, review_author, review_article, review_date)
            if len(review_title)>0:
                st.success("Post: {} saved" .format(review_title))
            else: 
                st.warning("Please add a review title")
        if st.button('Clear'):
            sessions=[review_writer, review_title, review_book, review_author, review_article, review_date]
            for session in sessions:
                session = ' '



    elif selected == "Search":
        st.subheader("Search Reviews")
        search_review= st.sidebar.text_input('Enter search term')
        search_choice= st.sidebar.radio("Search by", ("Review Author", "Review Title", "Book Title", "Book Author", "Publication Date"))

        if st.sidebar.button("Search"):
            if search_choice== "Review Author":
                category= 'writer'
            elif search_choice == "Review Title":
                category = 'title'
            elif search_choice == "Book Title":
                category = 'book'
            elif search_choice == "Book Author":
                category = 'author'
            elif search_choice == "Publication Date":
                category = 'date' 

            selected_post_search = get_search(category, search_review)

            for i in selected_post_search:
                display_writer = i[0]
                display_title = i[1]
                display_book = i[2] 
                display_author = i[3]
                display_article = i[4]
                display_date = i[5]

                st.markdown(selected_review_template.format(display_title,display_writer, display_book, display_author, display_date, display_article),  unsafe_allow_html=True) 


    elif selected == "Settings":
        st.subheader("Manage Reviews")


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


if __name__=='__main__':
    main()