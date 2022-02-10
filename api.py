import docker, random, time
from threading import Thread
#from utils import print_log

client = docker.from_env()

class API():
    def create_docker():
        # docker build -t "app:worker" .
        pass

    def kill(server, t):
        time.sleep(t-2)
        #server = server
        server.stop()
        server.remove()
        return 'stopped'

    def clear(name):
        try:
            server = client.containers.get(str(name))
            server.stop()
            server.remove()
        except:
            pass

    def stats(name,t):
        # beta
        cpu = 0
        mem = 0
        server = client.containers.get(str(name))
        while True:
            try:
                new_cpu = server.stats(stream=False)['cpu_stats']['cpu_usage']['total_usage']
                #print(new_cpu)
                if new_cpu != {}:
                    if cpu < new_cpu:
                        cpu = new_cpu
                new_mem = server.stats(stream=False)['memory_stats']['usage']
                #print(new_mem)
                if new_mem != {}:
                    if mem < new_mem:
                        mem = new_mem
            except docker.errors.APIError:
                break
            except docker.errors.NotFound:
                break
            except:
                pass
        if mem != 0: mem = int(mem)/8984
        return {"cpu": cpu, "mem": mem}

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
                "memory": '... MiB', # peak
                "CPUS": '...',
                "time": '... s'
            }
        }
        try:
            code = code.replace('"', '\\"')
            
            start_time = time.time()

            server = client.containers.run(
                "app:worker",
                f'python3 -c "{code}"',
                name=name,
                detach=True,
                mem_limit=f"{memory}m",
                cpu_count=cpus
            )
            kill = Thread(target=API.kill, args=(server,t))
            kill.start()
            #stats = Thread(target=API.stats, args=(name,t))
            #stats.start()

            #timestamps=True, 
            json['result'] = str(server.logs(tail=0, follow=True), 'UTF-8')

            json['usage']['time'] = f'{time.time() - start_time}s'

            #beta
            #stat = stats.join()
            #print(stats.join())
            #json['usage']['memory'] = f'{stat["mem"]}Mib'
            #json['usage']['CPUS'] = f'{stat["cpu"]}Mib'

            # статус(чтобы понять что убито выполнение кода)
            json['status'] = f'{kill.join()}'
            return json
        except Exception as e:
            print(e)
            try:
                json['result'] = str(server.logs(tail=0, follow=True), 'UTF-8')
            except:
                json['result'] = 'Omg... This code has not been run!'
                API.clear(name)
            return json

print(API.start('print(1)'))