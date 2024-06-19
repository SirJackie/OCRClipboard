import multiprocessing
import atexit
import time


class Subprocess:
    def __init__(self, ChildProcess):
        # Create Pipe Connection
        self.parent_conn, self.child_conn = multiprocessing.Pipe()
        self.process_name = ChildProcess.__name__

        # Create Sub-Process
        self.process = multiprocessing.Process(target=ChildProcess, args=(self.child_conn,))
        self.process.start()

        # Auto Destruction when Exit.
        atexit.register(self.Close)

    def Send(self, string):
        self.parent_conn.send(string)

    def Recv(self):
        while True:
            if self.parent_conn.poll():
                message = self.parent_conn.recv()
                return message
            time.sleep(0.01)

    def Close(self):
        # Terminate Sub-Process
        self.process.terminate()
        self.process.join()
        print("Subprocess Terminated. Process Name:", self.process_name)
