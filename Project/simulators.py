'''
This file contains the simulators for the algorithms. The simulators are used to generate the results for the paper.
'''


from utils import taskset_generator as gen_tasksets
from semi_partitioned_algos import DMPM, RMDP
from partitioned_algos import P_DM

def DMPM_Sim(num_tasksets,num_processors, util_min,util_max,system_util):
  """
  Simulates DMPM algorithm for 'num_tasksets' tasksets with 'num_processors' processors and returns the ratio of schedulable tasksets.

  Each taskset is generated so that total utilization is system_util*num_processors
  """

  tasksets=gen_tasksets(num_tasksets,util_min,util_max,system_util*num_processors,100,1000,'util')
  schedulable=0
  for taskset in tasksets:
    test=DMPM(taskset,num_processors)
    if(test.assign_tasks()):
      schedulable+=1
    #if(pdm_test.assign_tasks()):
    #  p_dm_schedulable+=1
  print("Schedulable=",schedulable)
  return schedulable/num_tasksets

def P_DM_Sim(num_tasksets,num_processors, util_min,util_max,system_util):
  """
  Simulates DMPM algorithm for 'num_tasksets' tasksets with 'num_processors' processors and returns the ratio of schedulable tasksets.

  Each taskset is generated so that total utilization is system_util*num_processors
  """
  tasksets=gen_tasksets(num_tasksets,util_min,util_max,system_util*num_processors,100,1000,'util')
  schedulable=0
  for taskset in tasksets:
    test=P_DM(taskset,num_processors)
    if(test.assign_tasks()):
      schedulable+=1
  return schedulable/num_tasksets

def RMDP_Sim(num_tasksets,num_processors, util_min,util_max,system_util):
  """
  Simulates DMPM algorithm for 'num_tasksets' tasksets with 'num_processors' processors and returns the ratio of schedulable tasksets.

  Each taskset is generated so that total utilization is system_util*num_processors
  """
  tasksets=gen_tasksets(num_tasksets,util_min,util_max,system_util*num_processors,100,1000,'dm')
  schedulable=0
  for taskset in tasksets:
    test=RMDP(taskset,num_processors)
    if(test.assign_tasks()):
      schedulable+=1
  return schedulable/num_tasksets



