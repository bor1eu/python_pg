import socket
import asyncio

class ServerError(Exception):
    pass

class ClientServerProtocol(asyncio.Protocol):
    data_safe = {}

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self._process_data(data.decode())
        self.transport.write(resp.encode())

    def _process_data(self, data):
        get_put, *params = data.strip("\n").split(" ")
        if get_put == "get" and len(params) == 1:
            name = params[0]
            # print(params)
            if name == "*":
                resp = self._resp_producer("ok", self.data_safe)
                # print(f"safe = {self.data_safe}")
            elif name not in self.data_safe:
                resp = self._resp_producer("ok")
            else:
                resp = self._resp_producer("ok", { name: self.data_safe[name]})

        elif get_put == "put" and len(params) == 3:
            name, value, timestamp = params
            try:
                value = float(value)
                timestamp = int(timestamp)
            except ValueError:
                return self._resp_producer("error", "wrong command")
            if name in self.data_safe:
                try:
                    idx = [x[0] for x in self.data_safe[name]].index(timestamp)
                    self.data_safe[name] = self.data_safe[name][:idx] + [(timestamp, value)] + self.data_safe[name][idx + 1:]
                except ValueError:
                    self.data_safe[name].append((timestamp, value))
                    self.data_safe[name].sort()
            else:
                self.data_safe[name] = [(timestamp, value)]
            
            resp = self._resp_producer("ok")
        else:
            resp = self._resp_producer("error", "wrong command")

        return resp

    def _resp_producer(self, status, raw_data = {}):
        resp = status +"\n"
        if type(raw_data) == str:
            resp += f"{raw_data}\n"
        elif type(raw_data) == dict:
            for key, value_list in raw_data.items():
                for record in value_list:
                    resp += f"{key} {record[1]} {record[0]}\n"
        else: 
            raise ServerError
        resp += "\n"

        return resp


def run_server(host, port):
    if host == False or port == False:
        raise ServerError
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == "__main__":
    run_server("127.0.0.1", 8888)
