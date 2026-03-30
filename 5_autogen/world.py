from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost
from agent import Agent
from creator import Creator
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
from autogen_core import AgentId
import messages
import asyncio
import os
os.environ["PYTHONIOENCODING"] = "utf-8"

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
HOW_MANY_AGENTS = 20

async def create_and_message(worker, creator_id, i: int):
    try:
        result = await worker.send_message(messages.Message(content=f"agent{i}.py"), creator_id)
        with open(f"idea{i}.md", "w") as f:
            f.write(result.content)
    except Exception as e:
        print(f"Failed to run worker {i} due to exception: {e}")

async def main():
    host = GrpcWorkerAgentRuntimeHost(address="localhost:50051")
    host.start() 
    worker = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    await worker.start()
    result = await Creator.register(worker, "Creator", lambda: Creator("Creator"))
    creator_id = AgentId("Creator", "default")
    coroutines = [create_and_message(worker, creator_id, i) for i in range(1, HOW_MANY_AGENTS+1)]
    await asyncio.gather(*coroutines) # run all the coroutines concurrently, which means we're creating and messaging all agents at the same time instead of waiting for each one to finish before starting the next one
    try:
        await worker.stop()
        await host.stop()
    except Exception as e:
        print(e)




if __name__ == "__main__":
    asyncio.run(main())


