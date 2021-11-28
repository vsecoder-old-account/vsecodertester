from memory_profiler import memory_usage
import subprocess, random, time
from threading import Thread
from mod.utils import print_log

class API():
    def create_docker():
        return subprocess.run(
            'docker build -t "app:worker" .', 
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
            shell=True, check=True
        ).stdout.decode('utf-8')

    def kill(name, t):
        time.sleep(t-2)
        try:
            res = subprocess.run(
                f'docker kill {name}', 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                shell=True, check=True
            ).stdout.decode('utf-8')
            return 'stopped'
        except Exception as e:
            print(e)
            return ''

    def clear():
        try:
            subprocess.run(
                f'docker image prune', 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                shell=True, check=True
            ).stdout.decode('utf-8')
        except:
            pass

    def stats():
        try:
            return subprocess.run(
                f'docker stats --no-stream', 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                shell=True, check=True
            ).stdout.decode('utf-8')
        except:
            return 'error'

    def start(code, lang, memory=50, cpus=0.1, t=5):
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
            command = {
                "py": "python -c",
                "js": "node -e",
                "bash": ""
            }
            code = code.replace('"', '\\"')
            timeout = Thread(target=API.kill, args=(name,t))
            timeout.start()
            print_log(f'docker run --name {name} --rm -m {memory}m --cpus={cpus} -it app:start {command[lang]} "{code}"', 'INFO', 'DOCKER')
            start_time = time.time()
            old_memory = memory_usage()[0]
            json['result'] = subprocess.run(
                f'docker run --name {name} --rm -m {memory}m --cpus={cpus} -it --network none app:worker {command[lang]} "{code}"', 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                shell=True, check=True, timeout=t+5
            ).stdout.decode('utf-8')
            json['usage']['time'] = f'{time.time() - start_time}s'
            json['usage']['memory'] = f'{memory_usage()[0] - old_memory}Mib'
            json['status'] = f'{timeout.join()}'
            return json
        except subprocess.CalledProcessError as e:
            json['result'] = str(e.output, 'UTF-8')
            print_log(json, 'INFO', 'DOCKER')
            return json
        except Exception as e:
            try:
                json['result'] = str(e.output, 'UTF-8')
            except:
                json['result'] = 'Omg... This code has not been run!'
                API.clear()
            if str(e)[:19] == f"Command 'docker run":
                json['result'] =  f'Code stoped after {t} seconds!'
                json['usage']['time'] = f'{t}s'
            print_log(json, 'INFO', 'DOCKER')
            return json
