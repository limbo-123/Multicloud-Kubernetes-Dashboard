import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

class ExecConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.namespace = self.scope['url_route']['kwargs']['namespace']
        self.pod_name = self.scope['url_route']['kwargs']['pod_name']
        self.container_name = self.scope['url_route']['kwargs']['container_name']

        await self.accept()

        try:
            # Asynchronously start the kubectl exec subprocess
            self.process = await asyncio.create_subprocess_exec(
                'kubectl', 'exec', '-i', self.pod_name, '-n', self.namespace, '-c', self.container_name, '--', 'sh',
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Create tasks to handle stdout and stderr from the process
            self.stdout_task = asyncio.create_task(self.listen_to_process_output(self.process.stdout))
            self.stderr_task = asyncio.create_task(self.listen_to_process_output(self.process.stderr))
        except Exception as e:
            await self.send(text_data=f"Error: {str(e)}")
            await self.close()

    async def listen_to_process_output(self, stream):
        try:
            # Continuously read from the process's output streams
            while True:
                line = await stream.readline()
                if line == b'':  # EOF
                    break
                await self.send(text_data=line.decode('utf-8'))
        except Exception as e:
            await self.send(text_data=f"Error reading from process: {str(e)}")

    async def receive(self, text_data):
        try:
            # Forward received input from WebSocket to the subprocess stdin
            if self.process and self.process.stdin:
                self.process.stdin.write(text_data.encode('utf-8') + b'\n')
                await self.process.stdin.drain()
        except BrokenPipeError:
            await self.send(text_data="Error: Broken pipe.")
        except Exception as e:
            await self.send(text_data=f"Error writing to process: {str(e)}")

    async def disconnect(self, close_code):
        # Terminate the process and cleanup on WebSocket disconnect
        if hasattr(self, 'stdout_task'):
            self.stdout_task.cancel()
        if hasattr(self, 'stderr_task'):
            self.stderr_task.cancel()
        if self.process:
            self.process.terminate()
            await self.process.wait()
