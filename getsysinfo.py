import os
import platform
import time
import psutil
import json

def deal2json(cls,json_data):
    return cls(
        pid=json_data['pid'],
        name=json_data['name'],
        cpu_percent=json_data['cpu_percent'],
        memory_percent=json_data['memory_percent'],
        cmdline=json.dumps(json_data['cmdline'])
    )
def get_cpu_info():
    cpuinfo = os.name
    #print("cpuinfo",cpuinfo)
    return cpuinfo
def get_system_info():
    systeminfo = platform.system()
    return systeminfo
def delay(n :  float):
    time.sleep(n)
    return print("delay",n,"s")
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)
def get_memory_usage():
    memory_total = psutil.virtual_memory().total
    memory_total_gb = memory_total / 1024 / 1024 /1024
    memory_available = psutil.virtual_memory().available
    memory_available_gb = memory_available / 1024 / 1024 /1024
    memory_used = memory_total - memory_available
    memory_used_gb = memory_used / 1024 / 1024 /1024
    memory_free = psutil.virtual_memory().free
    memory_free_gb = memory_free / 1024 / 1024 /1024
    memory_usage =  psutil.virtual_memory().percent
    return memory_total_gb,memory_available_gb,memory_used_gb,memory_free_gb,memory_usage
def get_PID():
    processes = []

    for pid in psutil.process_iter(
        {
        'pid',
        'ppid',
        'name',
        'username',
        'cpu_percent',
        'memory_percent',
        'cwd',
        'cmdline'
    }
    ):
        try:
            processes.append({
                    'pid':pid.info['pid'],
                    'ppid':pid.info['ppid'],
                    'name':pid.info['name'],
                    'username':pid.info['username'],
                    'cpu_percent':pid.info['cpu_percent'],
                    'memory_percent':pid.info['memory_percent'],
                    'cwd':pid.info['cwd'],
                    'cmdline':pid.info['cmdline']
                })
        except(psutil.NoSuchProcess,psutil.AccessDenied):
            continue
    return processes
            

    return pid
if __name__ == "__main__":
    #get_pid = get_PID()
    #print("get_pid",get_pid)
    cpuinfo = get_cpu_info()
    print("cpuinfo",cpuinfo)
    systeminfo = get_system_info()
    print("systeminfo",systeminfo)
    cpuusage = get_cpu_usage()
    print(f"cpu使用率{cpuusage}%")
    memoryusage = get_memory_usage()
    print(f"内存使用率{memoryusage[4]}%")
    print(f"内存总大小{memoryusage[0]:.2f}GB")
    print(f"内存可用大小{memoryusage[1]:.2f}GB")
    print(f"内存已用大小{memoryusage[2]:.2f}GB")
    print(f"内存剩余大小{memoryusage[3]:.2f}GB")
    old_cmdlines  = set()
    first_run = True
    try:
        while True:
            pidinfo = get_PID()
            with open("pidinfo.txt","w") as f:
                for pid in pidinfo:
                 f.write(str(pid)+"\n")
            
            str2cmdline = set ()

            for proc in pidinfo:
                cmdline = proc['cmdline'] or ()
                cmd_tuple = tuple(cmdline) 

                str2cmdline.add(cmd_tuple)
            if first_run:
                old_cmdlines = str2cmdline.copy()
                first_run = False
                delay(10)
                continue
            
            new_cmdlines = str2cmdline - old_cmdlines
            
            if new_cmdlines:
                with open("newpidinfo.txt","a") as f:
                    for pid in new_cmdlines:
                        f.write(
                            f"\n======{time.strftime('%Y-%m-%d %H:%M:%S')}发现新增进程命令行：{str(pid)} 新增进程记录===== \n"
                        )
                        for cmd in new_cmdlines:
                            meatching_procs = [p for p in pidinfo if tuple(p["cmdline"]) == cmd]
                            for proc in meatching_procs:
                                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}发现新增进程命令行：")
                                f.write(f"PID:{proc["pid"]} ")
                                f.write(f"PPID:{proc["ppid"]} ")
                                f.write(f"用户名:{proc["username"]} ")
                                f.write(f"进程名:{proc["name"]} ")
                                f.write(f"进程路径:{proc["cwd"]} ")
                                f.write(f"进程命令行:{proc["cmdline"]}\n")
                                #print(f"PID: {proc['pid']}")
                                #print(f"PPID: {proc['ppid']}")
                                #print(f"名称: {proc['name']}")
                                #print(f"用户名: {proc['username']}")
                                #print(f"CPU使用率: {proc['cpu_percent']}%")
                                #print(f"内存使用率: {proc['memory_percent']}%")
                                #print(f"工作目录: {proc['cwd']}")
                                #print(f"命令行: {' '.join(proc['cmdline'])}\n")
                                
            
                print(f"\n====={time.strftime('%Y-%m-%d %H:%M:%S')}发现新增进程命令行：=====\n")
                for cmd in new_cmdlines:
                    cmd_str = ''.join(cmd)
                    if cmd :
                        print(f"\n====={time.strftime('%Y-%m-%d %H:%M:%S')}发现新增进程命令行：=====\n")
                        print(cmd_str)
                    else:
                        print("无命令行")
            old_cmdlines = str2cmdline.copy()
            delay(10)

    except KeyboardInterrupt:
        print("\n程序终止")

      


    
