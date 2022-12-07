'''
Partitioned Scheduling Algorithms

Contains the following algorithms:
1. P-DM
2. FBB-FDD'''

import numpy as np
import math

class P_DM:
  '''
  Partitioned Deadline Monotonic Scheduling Algorithm

  P-DM assigns tasks based on first-fit heuristic for simplicity without sorting a task set.
  
  P-DM uses a response time analysis in the partitioning phase.
  
  Parameters
  ----------
  taskset : list
    List of tasks in the form of (execution time, period, priority)
  num_processor : int
    Number of processors in the system
      '''
  def __init__(self,taskset,num_processor):
    self.taskset=taskset
    self.num_processor=num_processor
    self.processor_tasks=[ [] for _ in range(num_processor) ]

  def getInterference(self,Ti,Tj):
  # Tj has higher priority than Ti
  # every task - (ei,pi) ; implicit deadline
    interference_ij_di = 0 
    ci,cj = Ti[0],Tj[0]
    pi,pj = Ti[1],Tj[1]
    di = pi
    F = math.floor(di/pj)
    if(di >= (F*pj+cj)):
      interference_ij_di = (F+1)*cj
    else: 
      interference_ij_di = di - F*(pj-cj)
    return interference_ij_di
  
  def get_Rik(self,Ti,k):
    R_ik = Ti[0]  # Execution time of task Ti
    # for a task(exTime,period,shared/not)
    #iterates over all the tasks in the processor k
    # for higher priority tasks find out the interference and add
    for Tj in self.processor_tasks[k] : 
      #if Tj is a shared task (Tj is higher priority)
      #if(Tj[2]==1):
        #R_ik += self.getInterference(Ti,Tj)
    # Tj not a shared task
      #else :
      if(Tj[2] <= Ti[2]):
        R_ik += self.getInterference(Ti,Tj)
    return R_ik
    
  def get_processor_tasks(self):
    return self.processor_tasks
    
  def get_proc_utils(self):
    utils=[]
    for k in range(self.num_processor):
      util=0
      for task in self.processor_tasks[k]:
        c,p,priority=task
        util+=(c/p)
      utils.append(util)
    return utils
    
  def assign_task_to_processor(self,task_to_assign):  
  #First fit heuristic
    for k in range(self.num_processor):
      Rik=self.get_Rik(task_to_assign,k)
      if(Rik<task_to_assign[1]):
        self.processor_tasks[k].append(task_to_assign)
        return True
    return False
  #(exec_time,period,priority,shared_task_or_not 0/1)   
  
  def assign_tasks(self):
    for task in self.taskset:
      #print('task=',task)
      if(self.assign_task_to_processor(task)==False):
        #print("Task cannot be scheduled")
        return False
    #all tasks are assigned
    #print("All tasks are assigned")
    #print(self.get_proc_utils())
    return True
  

class FBB_FDD:
  '''
  Fisher Baruah Baker- First Fit Decreasing Scheduler
  (Fisher et al., 2005)

  FBB-FDD sorts a task set in non-decreasing order of relative deadline, and assigns tasks to processors based on a first-fit heuristic
  
  FBB-FDD uses a polynomial time acceptance test in the partitioning phase.
  
  Parameters
  ----------
  taskset : list
    List of tasks in the form of (execution time, period, priority)
  num_processor : int
    Number of processors in the system
      '''
  def __init__(self,taskset,num_processor):
    self.taskset=taskset
    self.num_processor=num_processor
    self.processor_tasks=[ [] for _ in range(num_processor) ]
  
  def get_Rik(self,Ti,k):
    # Polynomial time acceptance test
    # Not implemented
    pass
    
  def get_processor_tasks(self):
    return self.processor_tasks
    
  def get_proc_utils(self):
    utils=[]
    for k in range(self.num_processor):
      util=0
      for task in self.processor_tasks[k]:
        c,p,priority=task
        util+=(c/p)
      utils.append(util)
    return utils
    
  def assign_task_to_processor(self,task_to_assign):  
  #First fit heuristic
    for k in range(self.num_processor):
      Rik=self.get_Rik(task_to_assign,k)
      if(Rik<task_to_assign[1]):
        self.processor_tasks[k].append(task_to_assign)
        return True
    return False
  #(exec_time,period,priority,shared_task_or_not 0/1)   

  #Function to sort taskset based on deadline
  def sort_taskset(self):
    self.taskset.sort(key=lambda x: x[1])
    print(self.taskset)
  
  def assign_tasks(self):
    self.sort_taskset()
    for task in self.taskset:
      print('task=',task)
      if(self.assign_task_to_processor(task)==False):
        print("Task cannot be scheduled")
        return False
    #all tasks are assigned
    print("All tasks are assigned")
    print(self.get_proc_utils())
    return True