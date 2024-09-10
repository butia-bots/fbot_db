from .redis_rag_inject import RedisRAGInject
from fbot_db.srv import RedisRagRetrieverSrv, RedisRagRetrieverSrvResponse

from langchain.docstore.document import Document
from langchain_redis import RedisConfig, RedisVectorStore

class RedisRAGRetriever(RedisRAGInject):
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
        response.context = [Document(page_content=doc.page_content) for doc in context]
        
        return response