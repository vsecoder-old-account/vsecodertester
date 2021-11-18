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
        time.sleep(t)
        try:
            subprocess.run(
                f'docker stop {name}', 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                shell=True, check=True
            ).stdout.decode('utf-8')
        except:
            pass

    def start(code, lang, memory=100, cpus=0.1, t=5):
        name = random.randrange(1, 999999999999999)
        json = {
            "id": name,
            "code": code,
            "result": '',
            "max": {
                "memory": f'{memory}MiB',
                "CPUS": f'{cpus}',
                "max_time": f"{t}s"
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
                "js": "node -e"
            }
            code = code.replace('"', '\\"')
            timeout = Thread(target=API.kill, args=(name,t))
            timeout.start()
            print_log(f'docker run --name {name} --rm -m {memory}m --cpus={cpus} -it app:worker {command[lang]} "{code}"', 'INFO', 'DOCKER')
            start_time = time.time()
            old_memory = memory_usage()[0]
            json['result'] = subprocess.run(
                f'docker run --name {name} --rm -m {memory}m --cpus={cpus} -it app:worker {command[lang]} "{code}"', 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                shell=True, check=True, timeout=t
            ).stdout.decode('utf-8')
            json['usage']['time'] = f'{time.time() - start_time}s'
            json['usage']['memory'] = f'{memory_usage()[0] - old_memory}Mib'
            print_log(json, 'INFO', 'DOCKER')
            if len(json['result']) > 10000:
                json['result'] = 'Sorry, but the code execution result is too long(>10.000).'
            return json
        except subprocess.CalledProcessError as e:
            json['result'] = str(e.output, 'UTF-8')
            print_log(json, 'INFO', 'DOCKER')
            return json
        except Exception as e:
            json['result'] = str(e.output, 'UTF-8')
            if str(e)[:19] == f"Command 'docker run":
                json['result'] =  f'Code stoped after {t} seconds!'
                json['usage']['time'] = f'{t}s'
            print_log(json, 'INFO', 'DOCKER')
            return json

API.create_docker()