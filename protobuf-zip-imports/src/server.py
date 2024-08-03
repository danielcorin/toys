import socket
import sys
from concurrent import futures
import grpc
import zipimport

# Import the generated code from gen.zip
importer = zipimport.zipimporter("gen.zip")
simple_pb2 = importer.load_module("simple_pb2")
simple_pb2_grpc = importer.load_module("simple_pb2_grpc")


class Greeter(simple_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return simple_pb2.HelloResponse(message=f"Hello, {request.name}!")


def serve(port=50051):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", port))
    except socket.error:
        print(f"Error: Port {port} is already in use")
        sys.exit(1)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    simple_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server started, listening on port {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
