'''
    Contains utility functions for generating tasksets.
    This file contains the code for generating tasksets using the Kato et al. algorithm.
'''


from task_generator import gen_periods_loguniform, gen_periods_uniform, gen_tasksets, gen_kato_utilizations
import numpy as np
def gen_periods_uniform_help(utils,min_, max_, round_to_int=False):
  """
    Helper function used to generate a list of random periods using a
    uniform distribution based on the size of 'utils' utilizations.

    Args:
        - `utils`: The 2D list of task utilizations.
        - `min_`: Period min.
        - `max_`: Period max.
  """ 
  #periods=[gen_periods_loguniform(len(utils[i]),1,min_=min_,max_=max_,round_to_int=round_to_int)[0] for i in range(len(utils))]
  periods=[gen_periods_uniform(len(utils[i]),1,min_=min_,max_=max_,round_to_int=round_to_int)[0] for i in range(len(utils))]
  #Change to gen_periods_loguniform if you want to use a log-uniform distribution
  return periods

def DM_sort(utils,periods):
  """
    Sorts the tasks in a taskset based on the DM algorithm.
    (Increasing order of periods)
  """
  utils_new=[]
  periods_new=[]
  for i in range(len(utils)):
    indices=np.argsort(periods[i])
    periods_new.append(np.array(periods[i])[indices].tolist())
    utils_new.append(np.array(utils[i])[indices].tolist())
  return utils_new,periods_new

def util_sort(utils,periods):
  """
    Sorts the tasks in a taskset based on the utilization in a non-increasing fashion.
  """
  utils_new=[]
  periods_new=[]
  for i in range(len(utils)):
    indices=np.argsort(utils[i])
    #indices in decreasing order
    indices=indices[::-1]
    periods_new.append(np.array(periods[i])[indices].tolist())
    utils_new.append(np.array(utils[i])[indices].tolist())
  return utils_new,periods_new

def priority_append_triplet(utils,periods,order='dm'):
  """
  Returns taskset with priority appended to each task

  Each task represented as a triplet (exec_time,period,priority)

  If order='dm' then tasks are ordered in increasing order of periods
  
  If order='util' then tasks are ordered in descending order of utilizations"""
  if(order=='dm'):
    utils,periods=DM_sort(utils,periods)
  elif(order=='util'):
    utils,periods=util_sort(utils,periods)
  tasksets=gen_tasksets(utils,periods)
  for each_taskset in tasksets:
    n=len(each_taskset)
    for i in range(n):
      task=each_taskset.pop(0)
      each_taskset.append((*task,i))
  return tasksets

def taskset_generator(nsets,umin,umax,target_util,period_min,period_max,order='dm'):
  """    
  Kato et al. tasksets generator.

    A task set Γ is generated as follows. A new periodic task is appended
    to Γ as long as U(Γ) ≤ Utot is satisfied. 
    
    For each task τi, its
    utilization Ui is computed based on a uniform distribution within the
    range of [Umin, Umax]. 
    
    Only the utilization of the task generated at the
    very end is adjusted so that U(Γ) becomes equal to Utot (thus the Umin
    constraint might not be satisfied for this task).

    Periods generated using a uniform distribution within the range of
    [Pmin, Pmax].

    Args:
        - `nsets`: Number of tasksets to generate.
        - `umin`: Minimum task utilization.
        - `umax`: Maximum task utilization.
        - `target_util`: Target utilization.
        - `period_min`: Minimum task period.
        - `period_max`: Maximum task period.
        - `order`: Task ordering. Either 'dm' or 'util'.

    If order='dm' then tasks are ordered in increasing order of periods.

    If order='util' then tasks are ordered in descending order of utilizations.

    Returns: A list containing 'nsets' of tasksets. Each taskset is a list of tasks. Each task is a
    tuple (exec_time, period, priority).
  """
  utils=gen_kato_utilizations(nsets,umin,umax,target_util)
  periods=gen_periods_uniform_help(utils,period_min,period_max)
  tasksets=priority_append_triplet(utils,periods,order)#Returns (exec_time, periods,priority)
  return tasksets