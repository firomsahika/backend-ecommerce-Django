from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
import requests
import xml.etree.ElementTree as ET
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import UnstructuredURLLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
import openai
import os
import logging


logger = logging.getLogger(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

def extract_urls_from_sitemap(sitemap):
    try:
        root = ET.fromstring(sitemap)
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [url.find("ns:loc", namespace).text for url in root.findall("ns:url", namespace)]
        return urls
    except ET.ParseError as e:
        logger.error(f"Error parsing sitemap: {e}")
        return []  # Return an empty list or handle the error as needed

class KnowledgeBase:
    def __init__(self, base_url: str, chunk_size: int, chunk_overlap: int):
        sitemap_url = f"{base_url}/sitemap.xml"
        logger.info(f"Loading sitemap from {sitemap_url}...")
        sitemap = requests.get(sitemap_url).text
        urls = extract_urls_from_sitemap(sitemap)

        logger.info(f"{len(urls)} URLs extracted.")
        logger.info("Loading URLs content...")
        loader = UnstructuredURLLoader(urls)
        data = loader.load()

        logger.info("Splitting documents into chunks...")
        doc_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = doc_splitter.split_documents(data)

        logger.info(f"{len(docs)} chunks created.")
        embeddings = OpenAIEmbeddings()
        docsearch = Chroma.from_documents(docs, embeddings)

        logger.info("Building the retrieval chain...")
        self.chain = RetrievalQAWithSourcesChain.from_chain_type(
            ChatOpenAI(),
            chain_type="map_reduce",
            retriever=docsearch.as_retriever(),
        )

    def ask(self, query: str):
        return self.chain({"question": query}, return_only_outputs=True)

@api_view(['POST'])
def chat(request):
    base_url = "http://127.0.0.1:8000/"  # Your website URL here
    kb = KnowledgeBase(base_url=base_url, chunk_size=8000, chunk_overlap=3000)
    
    user_query = request.data.get('query', '')
    response = kb.ask(user_query)
    
    return JsonResponse({'response': response})