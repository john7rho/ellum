# from langchain.vectorstores.faiss import FAISS
# from langchain.text_splitter import CharacterTextSplitter
# from langchain import VectorDBQA, OpenAI 
# from langchain.llms import HuggingFaceHub
# from langchain.embeddings import HuggingFaceEmbeddings
# from dotenv import load_dotenv
import modal
# from langchain.llms import NLPCloud
# load_dotenv()
# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# from tqdm import tqdm



# import modal

# stub = modal.Stub(image=modal.Image.debian_slim().pip_install("diskcache"))

# if stub.is_inside():
#     import diskcache as dc

#     cache = dc.Cache("/root/foo")

#     cache["rock"] = "zoom"


# @stub.function(shared_volumes={"/root/foo": modal.SharedVolume()})
# def expensive_computation(key: str):
#     cached = cache.get(key)

#     print(cached)

#     if cached is not None:
#         return cached

#     # populate_value





# def replaceNewLines(text):
#     return text.replace('\n', ' ').replace('\r', '')

# quote_page = "https://www.ketnipz.com/collections/shop-all"
# page = urlopen(quote_page)
# soup = BeautifulSoup(page)
# txt = replaceNewLines(soup.get_text())


stub = modal.Stub(
    
    "vectordbqaadi",
    image=modal.Image.debian_slim().pip_install(
        "aiohttp==3.8.4",
        "aiosignal==1.3.1",
        "anyio==3.6.2",
        "argilla==1.3.0",
        "async-timeout==4.0.2",
        "attrs==22.2.0",
        "backoff==2.2.1",
        "beautifulsoup4==4.11.2",
        "certifi==2022.12.7",
        "charset-normalizer==3.0.1",
        "click==8.1.3",
        "colorama==0.4.6",
        "dataclasses-json==0.5.7",
        "Deprecated==1.2.13",
        "et-xmlfile==1.1.0",
        "faiss-cpu==1.7.3",
        "filelock==3.9.0",
        "frozenlist==1.3.3",
        "greenlet==2.0.2",
        "h11==0.14.0",
        "httpcore==0.16.3",
        "httpx==0.23.3",
        "huggingface-hub==0.12.1",
        "idna==3.4",
        "joblib==1.2.0",
        "langchain==0.0.89",
        "libmagic==1.0",
        "lxml==4.9.2",
        "marshmallow==3.19.0",
        "marshmallow-enum==1.5.1",
        "monotonic==1.6",
        "multidict==6.0.4",
        "mypy-extensions==1.0.0",
        "nltk==3.8.1",
        "numpy==1.23.5",
        "openai==0.26.5",
        "openpyxl==3.1.1",
        "packaging==23.0",
        "pandas==1.5.3",
        "Pillow==9.4.0",
        "pydantic==1.10.5",
        "python-dateutil==2.8.2",
        "python-docx==0.8.11",
        "python-dotenv==0.21.1",
        "python-magic==0.4.27",
        "python-pptx==0.6.21",
        "pytz==2022.7.1",
        "PyYAML==6.0",
        "regex==2022.10.31",
        "requests==2.28.2",
        "rfc3986==1.5.0",
        "scikit-learn==1.2.1",
        "scipy==1.10.0",
        "sentence-transformers==2.2.2",
        "sentencepiece==0.1.97",
        "six==1.16.0",
        "sniffio==1.3.0",
        "soupsieve==2.4",
        "SQLAlchemy==1.4.46",
        "tenacity==8.2.1",
        "threadpoolctl==3.1.0",
        "tokenizers==0.13.2",
        "torch==1.13.1",
        "torchvision==0.14.1",
        "tqdm==4.64.1",
        "transformers==4.26.1",
        "typing-inspect==0.8.0",
        "typing_extensions==4.5.0",
        "unstructured==0.4.11",
        "urllib3==1.26.14",
        "wrapt==1.14.1",
        "XlsxWriter==3.0.8",
        "yarl==1.8.2",
        "diskcache==5.4.0"
),
)



# with open("output.txt", "w") as f:
#     for idx in tqdm(range(len(txt))):
#         token = txt[idx]
#         try:
#             f.write(token)
#         except:
#             pass
# txt = open("./output.txt").readlines()[0]




# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# texts = text_splitter.split_text(txt)

# embeddings = HuggingFaceEmbeddings()
# docsearch = FAISS.from_texts(texts, embeddings)
# # print(docsearch)
# print('docsearch done')

# nlpcloud = OpenAI()
# # nlpcloud = HuggingFaceHub(repo_id="google/byt5-large")
# print("nlp done")
# qa = VectorDBQA.from_chain_type(llm=nlpcloud, chain_type="stuff", vectorstore=docsearch)
# print('qa ready')
modalVolume = modal.SharedVolume().persist("ellum-vol")
if stub.is_inside():
    # import diskcache as dc

    # cache = dc.Cache("/root/foo")
    cache_path = "/root/foo/docsearch.pkl"

@stub.webhook(shared_volumes={"/root/foo": modalVolume}, keep_warm=True)
def queryurl(url: str):
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    from langchain.vectorstores.faiss import FAISS
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.embeddings import HuggingFaceEmbeddings
    import pickle
    print(url)
    def replaceNewLines(text):
        return text.replace('\n', ' ').replace('\r', '')

    quote_page = url
    page = urlopen(quote_page)
    soup = BeautifulSoup(page)
    txt = replaceNewLines(soup.get_text())
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_text(txt)

    embeddings = HuggingFaceEmbeddings()
    docsearch = FAISS.from_texts(texts, embeddings)
    print('docsearch done')
    print("saving DOCSEARCH INDEXER")
    with open(cache_path, "wb") as f:
        pickle.dump(docsearch, f)
    print("docsearch saved")

@stub.webhook(shared_volumes={"/root/foo": modalVolume}, secret=modal.Secret.from_name("my-openai-secret"), keep_warm=True)
def queryreal(x: str):
    from langchain import VectorDBQA, OpenAI
    import pickle
    print("libs imported")
    with open(cache_path, "rb") as f:
        docsearch = pickle.load(f)
    print("docsearch gotten")
    nlpcloud = OpenAI()
    print("nlp done")
    qa = VectorDBQA.from_chain_type(llm=nlpcloud, chain_type="stuff", vectorstore=docsearch)
    print('qa ready')
    return qa.run(x)


# @stub.webhook(secret=modal.Secret.from_name("my-openai-secret"))
# def query(x: str):
#     print(x)

#     def replaceNewLines(text):
#         return text.replace('\n', ' ').replace('\r', '')

#     quote_page = "https://www.ketnipz.com/collections/shop-all"
#     page = urlopen(quote_page)
#     soup = BeautifulSoup(page)
#     txt = replaceNewLines(soup.get_text())
#     text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     texts = text_splitter.split_text(txt)

#     embeddings = HuggingFaceEmbeddings()
#     docsearch = FAISS.from_texts(texts, embeddings)
#     # print(docsearch)
#     print('docsearch done')

#     nlpcloud = OpenAI()
#     # nlpcloud = HuggingFaceHub(repo_id="google/byt5-large")
#     print("nlp done")
#     qa = VectorDBQA.from_chain_type(llm=nlpcloud, chain_type="stuff", vectorstore=docsearch)
#     print('qa ready')

#     return qa.run(x)



# while True:
#     question = input("Question? ")
#     if (question == "@" or question == "q"):
#         break
#     else:
#         print(qa.run(question))