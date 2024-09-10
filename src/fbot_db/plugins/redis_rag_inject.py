from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_redis import RedisConfig, RedisVectorStore
from langchain.docstore.document import Document

import rospy

from .world_plugin import WorldPlugin
from fbot_db.srv import RedisRagInjectSrv

class RedisRAGInject(WorldPlugin):
    def __init__(self):
        super().init()
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.config = RedisConfig(
            index_name="quiz-context",
            redis_client=self.r,
        )
        self.vector_store = RedisVectorStore(self.embeddings, self.config)
    
    def run(self):
        rospy.Service('redis_rag_inject_srv', RedisRagInjectSrv, self._on_load_pdf)
        rospy.spin()
    
    def _separate_pdf_context(self, text):
        page_context = text[0].page_content
    
        # Split the text to get only the "Questions - context" part
        context_start = page_context.find("Questions - context")
        predefined_start = page_context.find("Questions Predefined")
        
        if context_start != -1 and predefined_start != -1:
            # Extract only the "Questions - context" section
            context_text = page_context[context_start:predefined_start]
            context_text = [Document(page_content=context_text)]
            
        else:
            print("Markers not found in the PDF file. Using full text as context.")
            context_text = text  # Fallback to full text if markers are not found
        
        return context_text
    
    def _injectToRedis(self, text):
        self.vector_store.add_documents(texts=text)
    
    def _on_load_pdf(self, req):
        try:
            pdf_path = req.pdf_path
            
            # Load and extract text from the PDF file
            loader = PyPDFDirectoryLoader(pdf_path)
            docs = loader.load()
            docs = self._separate_pdf_context(docs)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
            chunks = text_splitter.split_documents(docs)
            # Extract text content from each chunk
            texts = [chunk.page_content for chunk in chunks]
            self._injectToRedis(texts)
            
            return True
        
        except Exception as e:
            rospy.logerr(f"Failed to load PDF file: {pdf_path}")
            rospy.logerr(e)
            return False
        