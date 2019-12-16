# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 14:24:42 2019

@author: taha
"""

import psutil
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation



TIME_NUM = 100
FRAMES = 600
class ProcessMonitor:
    def  __init__(self, pids):
        self.cpu_nums = psutil.cpu_count()
        self.max_mem = psutil.virtual_memory().total

        self.plist = [psutil.Process(pid) for pid in pids]

        self.get_system_info()
        self.get_processes_info()

    def get_system_info(self):
        cpu_percent = psutil.cpu_percent(interval=0.0, percpu=False)
        mem_percent = float(psutil.virtual_memory().used) / self.max_mem * 100
        return cpu_percent, mem_percent

    def get_process_info(self, p):
        if p.is_running:
            cpu_percent = p.cpu_percent(interval=0.0) / self.cpu_nums
            mem_percent = p.memory_percent()
            #started_at = p.create_time()))      
        else:
            cpu_percent = 0.0
            mem_percent = 0.0
            #started_at = None
        return cpu_percent, mem_percent
    def get_processes_info(self):
        infodic = {}
        for p in self.plist:
            infodic[(p.pid, p.name)] = self.get_process_info(p)
        return infodic

class ProcessUsage:
    def __init__ (self, maxnum):
        
        self.maxnum = maxnum
        self.cpu_usage = []
        self.mem_usage = []
        self.times = []

    def update(self, num, cpu ,mem):
        self.cpu_usage.append(cpu)
        self.mem_usage.append(mem)

        if len(self.cpu_usage) > self.maxnum:
            self.cpu_usage = self.cpu_usage[1:]
            self.mem_usage = self.mem_usage[1:]
        else:
            self.times.append(num)
class ProcessGraph:
    def __init__(self,pids, username):
        self.taskmanager = ProcessMonitor(pids)
        self.username = username
    def __setData(self, usage, line):
        line.set_xdata(usage.times)
        line.set_ydata(usage.cpu_usage)
        
    def update_lines(self, num, sysline, sysUsage, plines, pUsages, ax):
        # get data from system
        sCpu , sMem = self.taskmanager.get_system_info()
        sysUsage.update(num, sCpu, sMem)
        self.__setData(sysUsage, sysline)
        # get data from Processes
        pInfos = self.taskmanager.get_processes_info()
        for (pid, name), ( cpu, mem) in pInfos.items():
            pUsage = pUsages[pid]
            pUsage.update(num, cpu, mem)
            pLine = plines[pid]
            self.__setData(pUsage, pLine)
        
        ax.set_xlim(0,100)
        ax.set_ylim(0,TIME_NUM)
        return sysline
    def find_user(self):
        for ss in psutil.users():
            if ss.name == self.username:
                return self.username
    def show(self):
        fig = plt.figure()
        ax = fig.gca(projection='rectilinear')
        #ax = plt.subplots(figsize=(18,5))
        # init axis
        ax.set_xlabel('Time')
        ax.set_ylabel('CPU Usage (%)')
        
        # System
        sysUsage = ProcessUsage(TIME_NUM)
        
        # sysline => blue and orange
        sysline, = plt.plot(sysUsage.times, sysUsage.cpu_usage)
        sysline.set_label('System')
        # Processes
        pUsages = {}
        pLines = {}
        info_dic = self.taskmanager.get_processes_info()
        print(info_dic.get('pid'))
        for (pid , name) , (cpu ,mem) in info_dic.items():
            pUsage = ProcessUsage(TIME_NUM)
            pline, = ax.plot(np.array(pUsage.times),np.array(pUsage.cpu_usage))
            
            pline.set_label('{0}({1})'.format(name, pid))
            
            pLines[pid] = pline
            pUsages[pid] = pUsage
            
        ax.legend()
        plt.title('Cpu Usage , Username: {0}'.format(self.find_user()))
        # Creating the Animation object
        line_ani = animation.FuncAnimation(fig, self.update_lines,FRAMES,
                                        fargs=(sysline, sysUsage, pLines, pUsages, ax),
                                        interval=100, blit=False,repeat=False)
        plt.show()
        line_ani.save('imo_frames1.htm')
# usage
pid1 = 8276
pid2 = 8276

graph = ProcessGraph([pid1, pid2], 'user19')
graph.show()