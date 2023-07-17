from signal import signal, SIGTERM
from concurrent import futures # grpc needs a thread pool
import random

import grpc 

from recommendations_pb2 import (
    BookCategory,
    BookRecommendation,
    RecommendationResponse
)
import recommendations_pb2_grpc


# Dummy data, in real microservice, we would serialize database objects into gRPC models
books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id=1, title="The Maltese Falcon"),
        BookRecommendation(id=2, title="Murder on the Orient Express"),
        BookRecommendation(id=3, title="The Hound of the Basketvilles"),
    ],
    BookCategory.SCIENCE_FICTION: [
        BookRecommendation(
            id=4, title="The Hitchiker's Guide to the Galaxy"
        ),
        BookRecommendation(id=5, title="Ender's Game"),
        BookRecommendation(id=6, title="The Dune Chronicles"),
    ],
    BookCategory.SELF_HELP: [
        BookRecommendation(
            id=7, title="The 7 Habits of Highly Effective People"
        ),
        BookRecommendation(
            id=7, title="How to Win Friends and Influence People"
        ),
        BookRecommendation(id=9, title="Man's Search for Meaning"),
    ]
}

class RecommendationService(
    recommendations_pb2_grpc.RecommendationsServicer
):
    def Recommend(self, request, context):
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found") # rpc status codes

        
        # get books in the requested category
        books_for_category = books_by_category[request.category]
        # get the number of possible recommendation requests
        num_results = min(request.max_results, len(books_for_category))
        # sample num_results from books_for category
        books_to_recommend = random.sample(
            books_for_category, num_results
        )


        # RecommendationResponse is a list of BookRecommendations
        return RecommendationResponse(recommendations=books_to_recommend)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
        RecommendationService(), server
    )

    with open("server.key", "rb") as fp:
        server_key = fp.read()
    with open("server.pem", "rb") as fp:
        server_cert = fp.read()

    with open("ca.pem", "rb") as fp:
        ca_cert = fp.read()
    
    # Send the 
    creds = grpc.ssl_server_credentials(
        [(server_key, server_cert)],
        root_certificates=ca_cert,
        require_client_auth=True,
    )


    server.add_secure_port("[::]:443", creds)
    # server.add_insecure_port("[::]:50051") # listen to all addresses on port 50051
    server.start()

    def handle_sigterm(*_):
        print("Received shutdown signal")
        all_rpcs_done_event = server.stop(30)
        all_rpcs_done_event.wait(30)
        print("Shut down gracefully")

    signal(SIGTERM, handle_sigterm)

    server.wait_for_termination()

if __name__ == "__main__":
    serve()
