'''
Semi-partitioned algorithms

Contains the following algorithms:
1. DMPM
2. RMDP'''


import numpy as np
import math

class DMPM:
  '''
  Deadline Monotonic with Priority Migration Scheduling Algorithm
  (Kato et al. 2008)

  DM-PM uses a response time analysis in the paritioning phase.
  
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
    self.num_tasks=np.shape(taskset)[0]
    #self.shared_tasks=[]
    #self.empty_processors=list(range(num_processor))
    self.proc_has_spare_capacity=[True for _ in range(num_processor)]
    self.taskSplitted=[False for _ in range(self.num_tasks)]
    self.cFracOfTaskSplittedPerProc=np.zeros((self.num_processor,self.num_tasks)).tolist()

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


  def split_task_across_processors(self,task_to_split):
    # Main function to split task across processors
    self.taskSplitted[task_to_split[2]]=True #Splitting task, priority=1
    c_req=task_to_split[0]
    c_sk=0
    x=0
    p_s=task_to_split[1]
    for k in range(self.num_processor):
      c_sk=0
      if(self.proc_has_spare_capacity[k]==False):
        #print("Processor ",k," has no spare capacity")
        continue
      #print("Processor ",k," has spare capacity")

      for task in self.processor_tasks[k]:
        c_i,d_i,i=task
        if (self.taskSplitted[i]==True):
          x=(d_i-self.cFracOfTaskSplittedPerProc[k][i])/(math.ceil(d_i/p_s))
        else:
          x=(d_i-self.get_Rik(task,k))/(math.ceil(d_i/p_s))
        if((x>c_sk)):
          if(x>0):
            c_sk=x
      if(c_sk!=0):
        c_req=c_req-c_sk
        #self.processor_tasks[k].append((c_sk,p_s,task_to_split[2]))
        if(c_req==0):
          self.proc_has_spare_capacity[k]=False
          self.cFracOfTaskSplittedPerProc[k][task_to_split[2]]=c_sk
          return True
        elif(c_req<0):
          c_sk=c_sk+c_req
          self.cFracOfTaskSplittedPerProc[k][task_to_split[2]]=c_sk
          return True
        else:
          self.cFracOfTaskSplittedPerProc[k][task_to_split[2]]=c_sk
      self.proc_has_spare_capacity[k]=False
    return False
        

    
  
  def assign_tasks(self):
    for task in self.taskset:
      print('task=',task)
      if(self.assign_task_to_processor(task)==False):
        #task not assigned to any processor
        #split the task
        print('Splitting task',task)
        if(self.split_task_across_processors(task)==False):
          #task is not schedulable
          print("Task cannot be scheduled")
          print(self.get_proc_utils())
          return False
    #all tasks are assigned
    print("All tasks are assigned")
    #print(self.get_proc_utils())
    return True


class RMDP:
  '''
  Rate Monotonic Deferrable Portion Scheduling Algorithm 
  (Kato et al. 2008)

  Highest priority assigned to migratory tasks, fixed tasks have RM priority.

  RMDP uses Liu and Layland's bound to schedule fixed tasks and then
  the remaining tasks are split and allowed to migrate based on the 
  Liu and Layland bound.
  
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
    self.num_tasks=np.shape(taskset)[0]
    #self.shared_tasks=[]
    #self.empty_processors=list(range(num_processor))
    self.proc_has_spare_capacity=[True for _ in range(num_processor)]
    self.taskSplitted=[False for _ in range(self.num_tasks)]
    self.cFracOfTaskSplittedPerProc=np.zeros((self.num_processor,self.num_tasks)).tolist()
    
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
  
  def get_proc_util_proc_k(self,k):
    return self.get_proc_utils()[k]

  def liu_bound(self,k,task):
    c,p,priority=task
    U= (self.get_proc_util_proc_k(k)+c/p)
    #number of tasks in processor k
    n=len(self.processor_tasks[k])+1
    if(U<=n*(2**(1/n)-1)):
      return True
    else:
      return False
    
  def assign_task_to_processor(self,task_to_assign):  
  #First fit heuristic
    for k in range(self.num_processor):
      if(self.liu_bound(k,task_to_assign)):
        self.processor_tasks[k].append(task_to_assign)
        return True
    return False
  #(exec_time,period,priority,shared_task_or_not 0/1)


  def split_task_across_processors(self,task_to_split):
    self.taskSplitted[task_to_split[2]]=True #Splitting task, priority=1
    c_req=task_to_split[0]
    c_sk=0
    x=0
    p_s=task_to_split[1]
    for k in range(self.num_processor):
      c_sk=0
      if(self.proc_has_spare_capacity[k]==False):
        #print("Processor ",k," has no spare capacity")
        continue
      #print("Processor ",k," has spare capacity")
      #get processor utilisation
      U_k=self.get_proc_util_proc_k(k)
      #get number of tasks in processor k
      n_k=len(self.processor_tasks[k])
      U_sk=U_k-(n_k+1)*(2**(1/(n_k+1))-1)
      #If U_sk is positive, there is a possibility of splitting the task
      #If U_sk is negative, there is no possibility of splitting the task
      #c_sk=U_sk*p_s
      #subtract c_sk from c_req
      #c_req=c_req-c_sk
      #if c_req is negative, return true
      #else, continue to next processor
      if(U_sk>0):
        c_sk=U_sk*p_s
        c_req-=c_sk
        if(c_req<=0):
          self.cFracOfTaskSplittedPerProc[k][task_to_split[2]]=c_sk
          return True
        else:
          self.cFracOfTaskSplittedPerProc[k][task_to_split[2]]=c_sk
          self.proc_has_spare_capacity[k]=False
      else:
        self.proc_has_spare_capacity[k]=False  
    return False
        
  
  def assign_tasks(self):
    for task in self.taskset:
      #print('task=',task)
      if(self.assign_task_to_processor(task)==False):
        #task not assigned to any processor
        #split the task
        #print('Splitting task',task)
        if(self.split_task_across_processors(task)==False):
          #task is not schedulable
          #print("Task cannot be scheduled")
         # print(self.get_proc_utils())
          return False
    #all tasks are assigned
    #print("All tasks are assigned")
   # print(self.get_proc_utils())
    return True
  