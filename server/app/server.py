# app/server.py
import asyncio
import websockets
import json
import time
from .input_handler import InputHandler
from .config import HOST, PORT

class WebSocketServer:
    def __init__(self, status_callback):
        self.loop = None
        self.stop_event = None
        self.status_callback = status_callback
        self.input_handler = InputHandler()

    async def echo(self, websocket):
        self.status_callback("Подключение есть")
        try:
            while True:
                # Таймаут для инерции скролла можно добавить сюда
                message = await websocket.recv()
                spec = json.loads(message)

                if spec.get("ping", False):
                    await websocket.send(json.dumps({"pong": True}))
                    continue

                if "altTab" in spec:
                    self.input_handler.handle_alt_tab(spec["altTab"])
                    continue

                if spec.get('scroll', False):
                    self.input_handler.handle_scroll(spec.get('scrollY', 0))
                    self.status_callback("Подключение есть, скролл")
                    continue
                else:
                    self.input_handler.reset_scroll()

                # Движение
                if 'x' in spec and 'y' in spec:
                    self.input_handler.process_movement(spec['x'], spec['y'])
                    self.status_callback("Подключение есть, курсор")

                # Клики
                self.input_handler.process_clicks(
                    spec.get('click', False),
                    spec.get('right_click', False)
                )

        except websockets.ConnectionClosed:
            self.status_callback("Ожидание")
        except Exception as e:
            print(f"Server Error: {e}")
        finally:
            self.input_handler.cleanup()

    def start(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.stop_event = asyncio.Event()

        async def server_main():
            self.status_callback("Ожидание")
            async with websockets.serve(self.echo, HOST, PORT):
                await asyncio.Future() # run forever

        try:
            self.loop.run_until_complete(server_main())
        except Exception as e:
            print("Server loop error:", e)
        finally:
            self.loop.close()

    def stop(self):
        if self.loop:
            self.loop.call_soon_threadsafe(self.stop_event.set)