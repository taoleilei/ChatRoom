import socket
import select
import string
import sys


def prompt():
    # 标准屏幕输出
    sys.stdout.write("<You> ")
    sys.stdout.flush()

if __name__ == '__main__':
    # 判断用户是否正确运行程序，要求IP，端口。类似python client.py localhost 5000
    if (len(sys.argv) < 3):
        print('Usage : python client.py hostname port')
        sys.exit()
    # 获取用户输入的IP
    host = sys.argv[1]
    # 获取用户输入的端口
    port = int(sys.argv[2])
    # 创建连接服务器的socket链接
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置超时时间2秒
    s.settimeout(2)

    try:
        # 尝试连接
        s.connect((host, port))
    except:
        print("unable to connect")
        sys.exit()

    print('Connected to remote host. Start sending messages')
    prompt()

    while True:
        # 这里有两个 I/O 事件需要监听：连接到服务器的 socket 和标准输入，同样我们可以使用 select 来完成
        socket_list = [sys.stdin, s]

        read_sockets, write_sockets, error_sockets = select.select(
            socket_list, [], [])
        # 循环可读事件
        for sock in read_sockets:
            # 如果是与服务器连接的 socket 有数据可读，表示服务器发送消息给该客户端，那么就从 socket 接收数据
            if sock == s:
                data = sock.recv(1024)
                # 没有数据
                if not data:
                    print('\nDisconnected from chat server')
                    sys.exit()
                else:
                    data_str = data.decode('utf-8')
                    sys.stdout.write(data_str)
                    prompt()
            else:
                # sys.stdin 有数据可读，表示用户从控制台输入数据并按下回车，那么就从标准输入读数据，并发送到服务器
                msg = sys.stdin.readline()
                msg_bytes = msg.encode(encoding='utf-8')
                s.send(msg_bytes)
                prompt()


'''
python client.py localhost 5000
'''
