import docker, random, time
from threading import Thread
import concurrent.futures

client = docker.from_env()

class API():
    def create_docker():
        # docker build -t "app:worker" .
        pass

    def kill(server, t):
        time.sleep(t)
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

    def stats(name, t):
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
                if mem != 0: mem = int(mem)/8984
                return {"cpu": cpu, "mem": mem} 
            except docker.errors.NotFound:
                if mem != 0: mem = int(mem)/8984
                return {"cpu": cpu, "mem": mem} 
            except:
                pass

    def start(code, memory=512, cpus=1, network_disabled=True, t=5):
        name = random.randrange(1, 999999999999999)
        # шаблон результата
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
            
            # https://docker-py.readthedocs.io/en/stable/containers.html
            server = client.containers.run(
                "app:worker",
                f'python3 -c "{code}"',
                name=name,
                detach=True,
                mem_limit=f"{memory}m",
                network_disabled=network_disabled,
                cpu_count=cpus
            )

            # отвечает за убийство процесса в случаи долгого выполнения
            kill = Thread(target=API.kill, args=(server,t))
            kill.start()

            #timestamps=True, - можно добавить для тайм кодов в результате
            json['result'] = str(server.logs(tail=0, follow=True), 'UTF-8')

            # время выполнения
            json['usage']['time'] = f'{time.time() - start_time}s'

            # beta
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(API.stats, name, t)
                return_value = future.result()
                json['usage']['memory'] = f'{return_value["mem"]}Mib'
                json['usage']['CPUS'] = f'{return_value["cpu"]}'

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

print(
    API.start(
        'for i in range(1, 200): print(1)', # python code(str)
        memory=512,                         # память(в МБ) максимально доступная для выполнения(int)
        cpus=1,                             # кол-во ядер для выполнения(int)
        network_disabled=False,             # блокировка интернета (bool)
        t=5                                 # максимальное среднее время выполнения(int)
    )
)

# result =>

#{
#    'id': 534403284476367,            -- id
#    'code': 'print(1)',               -- python code
#    'result': '1\n',                  -- result
#    'status': 'None',                 -- status(if stopped - process killed)
#    'max': {                          -- limitations
#        'memory': '512MiB', 
#        'CPUS': '1', 
#        'time': '5s'
#    }, 
#    'usage': {
#        'memory': '0Mib',             -- usage peak (> 1 MB)
#        'CPUS': '0',                  -- usage peak (> 1)
#        'time': '0.6736643314361572s' -- execution time
#    }
#}