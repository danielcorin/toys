import grpc
import zipimport

# Import generated code from zip file
importer = zipimport.zipimporter("gen.zip")
simple_pb2 = importer.load_module("simple_pb2")
simple_pb2_grpc = importer.load_module("simple_pb2_grpc")


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = simple_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(simple_pb2.HelloRequest(name="World"))
        print(f"Greeter client received: {response.message}")


if __name__ == "__main__":
    run()
