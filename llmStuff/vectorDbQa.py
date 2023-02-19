from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain import VectorDBQA, OpenAI 
from langchain.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
# from langchain.llms import NLPCloud
load_dotenv()
txt = open("./output.txt").readlines()[0]
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(txt)

embeddings = HuggingFaceEmbeddings()
docsearch = FAISS.from_texts(texts, embeddings)
# print(docsearch)

nlpcloud = OpenAI()
qa = VectorDBQA.from_chain_type(llm=nlpcloud, chain_type="stuff", vectorstore=docsearch)
print(qa.run("Summarize this"))
while True:
    question = input("Question? ")
    if (question == "@" or question == "q"):
        break
    else:
        print(qa.run(question))