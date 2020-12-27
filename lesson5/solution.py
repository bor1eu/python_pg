import socket
import time

class ClientError(Exception):
    pass

class Client():
    def __init__(self, srv_address, port_number, timeout = None):
        self.sock = socket.create_connection((srv_address, port_number), timeout)
        # pass

    def get(self, metrics_name):
        query = self._query_string("get", metrics_name)
        # print(query)
        try:
            self.sock.send(query.encode("utf8"))
            # resp = self.sock.recv(1024).decode("utf-8")
            resp = self._parse_resp(self.sock.recv(1024).decode("utf-8"))
            return resp
            # data = "ok\npalm.cpu 2.0 1150864247\npalm.cpu 0.5 1150864248\neardrum.cpu 3.0 1150864250\n\n"
        # except socket.timeout:
        #     print("send data timeout")
        except socket.error as ex:
            raise ClientError
            # print("send data error:", ex)
        # resp = self._parse_resp(resp)
        # print(resp)
        # return resp

    def put(self, metrics_name, metrics_value, timestamp = None):
        if timestamp is None:
            timestamp = int(time.time())
        query = self._query_string("put", metrics = metrics_name, value = metrics_value, metrics_timestamp=timestamp)
        # print(query)
        try:
            self.sock.send(query.encode("utf8"))
            # resp = self.sock.recv(1024).decode("utf-8")
            resp = self._parse_resp(self.sock.recv(1024).decode("utf-8"))
            # pass
        # except socket.timeout:
        #     print("send data timeout")
        except socket.error as ex:
            raise ClientError
            # print("send data error:", ex)

    def _query_string(self, get_put_string, metrics, value = None, metrics_timestamp = None):
        if get_put_string == "put":
            # print(value)

            # value = str(value)
            params = map(str, ["put", metrics, value, metrics_timestamp])
        elif get_put_string == "get":
            params = ["get", metrics]
        return " ".join(params) + '\n'

    def _list_append_sort(self, arr, item):
        arr.append(item)
        return sorted(arr, key=lambda elem: elem[0])
    
    def _parse_resp(self, srv_rsp):
        status, *data_input = srv_rsp.split('\n')
        data_output = {}
        if status == "ok":
            for item in data_input:
                if item != "":
                    try:
                        name, value, timestamp = item.split(' ')
                        value = float(value)
                        timestamp = int(timestamp)
                    except ValueError:
                        raise ClientError
                    if name in data_output:
                        data_output[name] = self._list_append_sort(data_output[name], (timestamp, value))
                        # data_output[temp[0]] = data_output[temp[0]].append((float(temp[1]),int(temp[2])))
                    else:
                        data_output[name] = [(timestamp, value)]
                else:
                    break
            return data_output
        elif status == "error":
            raise ClientError
        else:
            raise ClientError

if __name__ == "__main__":
    client = Client("127.0.0.1", 8888, timeout=15)
    client.put("palm.cpu", 0.5, timestamp=1150864247)
    client.put("palm.cpu", 2.0, timestamp=1150864248)
    client.put("palm.cpu", 0.5, timestamp=1150864248)
    client.put("eardrum.cpu", 3, timestamp=1150864250)
    client.put("eardrum.cpu", 4, timestamp=1150864251)
    client.put("eardrum.memory", 4200000)
    print(client.get("*"))