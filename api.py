from memory_profiler import memory_usage
import docker, random, time
from threading import Thread
#from utils import print_log

client = docker.from_env()

class API():
    def create_docker():
        # docker build -t "app:worker" .
        pass

    def kill(name, t):
        time.sleep(t-2)
        server = client.containers.get(str(name))
        server.stop()
        server.remove()
        return 'stopped'

    def clear(name):
        server = client.containers.get(str(name))
        server.stop()
        server.remove()

    def stats():
        pass

    def start(code, memory=512, cpus=1, t=5):
        name = random.randrange(1, 999999999999999)
        json = {
            "id": name,
            "code": code,
            "result": '',
            "status": '',
            "max": {
                "memory": f'{memory}MiB',
                "CPUS": f'{cpus}',
                "time": f"{t}s"
            },
            "usage": {
                "memory": '... MiB',
                "CPUS": '...',
                "time": '... s'
            }
        }
        try:
            code = code.replace('"', '\\"')
            timeout = Thread(target=API.kill, args=(name,t))
            timeout.start()
            
            start_time = time.time()
            old_memory = memory_usage()[0]

            server = client.containers.run(
                "app:worker",
                f'python3 -c "{code}"',
                name=name,
                detach=True,
                mem_limit=f"{memory}m",
                cpu_count=cpus
            )

            #print(server.stats())

            #timestamps=True, 
            json['result'] = str(server.logs(tail=0, follow=True), 'UTF-8')

            json['usage']['time'] = f'{time.time() - start_time}s'
            # костыль убрать через server.stats()
            json['usage']['memory'] = f'{memory_usage()[0] - old_memory}Mib'
            # статус(чтобы понять что убито выполнение кода)
            json['status'] = f'{timeout.join()}'
            return json
        except Exception as e:
            print(e)
            try:
                json['result'] = str(e.output, 'UTF-8')
            except:
                json['result'] = 'Omg... This code has not been run!'
                API.clear(name)
            return json

#print(API.start('for i in range(1, 200): print(1)'))