import socket
import select

def broadcast_data(sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock:
            try:
                socket.send(message)
            except:
                socket.close()
                CONNECTION_LIST.remove(socket)
if __name__ == '__main__':
    # 定义一个 list 型变量 CONNECTION_LIST 表示监听多个 socket 事件的可读事件
    CONNECTION_LIST = []
    RECV_BUFFER = 1024
    PORT = 5000
    # 创建socket连接
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定IP，端口
    server_socket.bind(("0.0.0.0", PORT))
    # 监听
    server_socket.listen(10)

    CONNECTION_LIST.append(server_socket)

    print("Chat server started on port " + str(PORT))

    while True:
        # select 方法的三个参数都是 list 类型，分别代表读事件、写事件、错误事件，同样方法返回值也是三个 list，包含的是哪些事件（读、写、异常）满足了
        read_sockets, write_sockets, error_sockets = select.select(
            CONNECTION_LIST, [], [])
        # 循环可读事件
        for sock in read_sockets:
            # 如果是主 socket（即服务器开始创建的 socket，一直处于监听状态）有数据可读，表示有新的连接请求可以接收，此时需要调用 accept 函数来接收新的客户端连接，并将其连接信息广播到其它客户端。
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print("Client (%s, %s) connected" % addr)
                msg = "[%s:%s] entered roomn" % addr
                msg_bytes = msg.encode(encoding='utf-8')
                broadcast_data(sockfd, msg_bytes)
            else:
                # 如果是其它 sockets（即与客户端已经建立连接的 sockets）有数据可读，那么表示客户端发送消息到服务器端，使用 recv 函数读消息，并将消息转发到其它所有连接的客户端
                try:
                    data = sock.recv(RECV_BUFFER)
                    # 接受到的data是字节类型
                    if data:
                        broadcast_data(sock, data)
                except:
                    msg = "Client (%s, %s) is offline" % addr
                    msg_bytes = msg.encode(encoding='utf-8')
                    broadcast_data(sock, msg_bytes)
                    print("Client (%s, %s) is offline" % addr)
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
    server_socket.close()


'''
python server.py
'''