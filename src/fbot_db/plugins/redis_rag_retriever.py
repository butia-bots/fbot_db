from .redis_rag_injector import RedisRAGInjector
from fbot_db.srv import RedisRagRetrieverSrv, RedisRagRetrieverSrvResponse

from langchain.docstore.document import Document

import rospy

class RedisRAGRetriever(RedisRAGInjector):
    def __init__(self):
        super().__init__()
        self.retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 12})

    def run(self):
        rospy.Service('redis_rag_retriever_srv', RedisRagRetrieverSrv, self._retrieve_from_redis)
        rospy.spin()
        
    def _retrieve_from_redis(self, req) :
        question = req.question
        k = req.k
        retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})
        
        # Retrieve relevant documents
        context = retriever.get_relevant_documents(question)
        
        response = RedisRagRetrieverSrvResponse()
        # Extract the page_content and metadata from each document
        response.page_contents = [doc.page_content for doc in context]
        response.metadata = [str(doc.metadata) for doc in context]  # Convert metadata to string if needed
        
        return response