from .redis_rag_inject import RedisRAGInject

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
        answer = retriever.get_relevant_documents(question)
        return answer # [Document]