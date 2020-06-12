from flask import Flask, render_template, request
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import * #import Schema TEXT ID
import os.path
app = Flask(__name__)

# open and render the demo1.html
# use route to tell Flask what URL should trigger our function
@app.route('/')
def student():
  return render_template('demo1.html')

# handle the data that the user had input to the box on html
@app.route('/result',methods = ['POST', 'GET'])
def search():
  # check if there is a post request from user
  if request.method == 'POST':

    # 'words' is the name I defined for the input : see demo1.html
    # store the user's input to user_result
    user_result = request.form['words']

    ##################### main search code starts here ##############
    # schema specifies the fields of documents in an index
    # each document can have multiple fields, so field value is available in search results
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)

    # this creates a storage object to contain the index
    # index is the object to store documents
    if not os.path.exists("index"):
      os.mkdir("index")
    ix = create_in("index",schema)

    # open the index just created
    ix = open_dir("index")

    # open the file that contains paper abstracts
    # f = open('/Users/mac/Downloads/arxiv-abstracts-250k.txt', 'r')
    f = open('/Users/mac/Downloads/folder/small_abstract.txt', 'r')

    # read the file by lines
    line = f.readlines()

    # add document to index with writer()
    # defualt：128 Setting it higher can speed up indexing
    # only one thread/process at a time can have a writer open
    writer = ix.writer(limitmb = 256)

    # to count the number of asbstract
    index = 0

    # see each line as a document and add to the index object
    for each_abs in line:
      final_title = "Abstract" + str(index) + ":" + each_abs
      writer.add_document(title = final_title, content = each_abs)
      index = index + 1

    # to commit the docs we just added
    writer.commit()

    # to obtain the searcher object
    searcher = ix.searcher()

    # to find the abstract that contains the key words
    # format: title and content
    results = searcher.find("content", str(user_result))

    # show the total number of abstracts that contain the key words
    result_string = "There are " + str(len(results)) + " results based on your key word"

    # create a result list that can be displayed in the result page
    r = []
    r.append(result_string)
    # convert the result type to a list type
    for each_result in results:
      r.append(each_result)

    # do not forget to close the file we opened
    f.close()

    # open and render the result.html
    return render_template("result.html",result = r)

# run the application on the local development server
if __name__ == '__main__':
  app.run(debug = True)