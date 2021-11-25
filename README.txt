How to run:

  - First, install the recommended planner on the page website, Fast Downward:
      www.fast-downward.org

  - After setting up the planner, move to its main folder both domain file and proj1.py

  - Finally, simply run the python file with:
      python3 proj1.py < input_file > output_file

  - As asked, the results will be in the output_file


Features:

  Our file proj1.py receives the input from the input file and creates the instance file, accordingly.
  On the other hand, the domain file is static, meaning that it does not need to be created by the main file
  and does not change from instance to instance.


  The domain file has types, predicates, functions and one action.

  We define 2 types, "machine" and "task".

  We used the predicates:
    -> next_machine - indicates the next machine
    -> prev_machine - its valid if the machine p_m was the last used
    -> on_machine - its valid if the task can be scheduled on the machine
    -> must-be-first - its valid if t is the first subtask of its task
    -> must-be-done - its valid the task t2 depends on task t1
    -> must-be-next - its valid if the subtask t2 comes immediately after t1
    -> done - its valid if the subtask t is finished
    -> None - its valid if the task is a None task
    -> prev_task - its valid if the task t was the last task scheduled in machine m
    -> freshly_done - its valid if the task t was finished in the current point in time

  The function "total_cost" its a number that is increased for every scheduled task.

  The action "schedule_task" receives as parameters the previous and current machines
  and the previous and current tasks.
  Checks if the current machine is the correct one and if the task respects the correct conditions to be scheduled.
  After that, changes the predicates in order schedule the next task and increments the total cost by 1.
