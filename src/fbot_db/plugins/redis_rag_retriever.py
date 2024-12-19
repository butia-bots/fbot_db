from .redis_rag_injector import RedisRAGInjector
from fbot_db.srv import RedisRagRetrieverSrv

from langchain.docstore.document import Document

import rclpy
from rclpy.node import Node

class RedisRAGRetriever(RedisRAGInjector):
    def __init__(self):
        super().__init__()
        self.retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 12})
        self.srv = self.create_service(RedisRagRetrieverSrv, 'redis_rag_retriever_srv', self._retrieve_from_redis)

    def _retrieve_from_redis(self, req, res):
        question = req.question
        k = req.k
        retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})
        
        # Retrieve relevant documents
        context = retriever.get_relevant_documents(question)
        
        # Extract the page_content and metadata from each document
        res.page_contents = [doc.page_content for doc in context]
        res.metadata = [str(doc.metadata) for doc in context]  # Convert metadata to string if needed
        
        return res