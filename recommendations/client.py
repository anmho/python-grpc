import grpc
from recommendations_pb2_grpc import RecommendationsStub
from recommendations_pb2 import BookCategory, RecommendationRequest
channel = grpc.insecure_channel("localhost:50051")
client = RecommendationsStub(channel)
request = RecommendationRequest(
	user_id=1, category=BookCategory.SCIENCE_FICTION, max_results=2)
recommendations = client.Recommend(request)

print(recommendations)


