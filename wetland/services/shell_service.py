def shell_service(hacker_session, docker_session, output):

    hacker_session.settimeout(3600)
    output.o('content', 'shell', "N"*20)

    try:
        while True:
            if hacker_session.recv_ready():
                text = hacker_session.recv(1)
                docker_session.sendall(text)
                output.o('content', 'shell', '[H]:'+text.encode("hex"))

            if docker_session.recv_ready():
                text = docker_session.recv(1024)
                output.o('content', 'shell', '[V]:'+text.encode("hex"))
                hacker_session.sendall(text)

            if docker_session.recv_stderr_ready():
                text = docker_session.recv_stderr(1024)
                hacker_session.sendall_stderr(text)

            if docker_session.eof_received:
                hacker_session.shutdown_write()
                hacker_session.send_exit_status(0)
                break

            if hacker_session.eof_received:
                break

    except Exception, e:
        print e
    finally:
        hacker_session.close()
        docker_session.close()