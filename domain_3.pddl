(define (domain tasksworld)

    (:requirements :adl :action-costs)

    (:types machine task)

    (:predicates (next_machine ?p_m ?m - machine)
                 (prev_machine ?m - machine)
                 (on_machine ?t - task ?m - machine)
                 (must-be-first ?t - task)
                 (must-be-done ?t1 ?t2 - task)
                 (must-be-next ?t1 ?t2 - task)
                 (done ?t - task)
                 (None ?t - task)
                 (prev_task ?t - task ?m - machine)
                 (freshly_done ?t - task)
    )


    (:functions (total-cost) - number)

    (:action schedule_task

      :parameters (?p_m ?m - machine ?p_t ?t - task)

      :precondition (and (prev_machine ?p_m)
                         (next_machine ?p_m ?m)
                         (prev_task ?p_t ?m)
                         (or (must-be-next ?t ?p_t)
                             (and (must-be-first ?t)
                                  (on_machine ?t ?m)
                                  (not (done ?t))
                                  (exists (?d_t - task)
                                    (and (must-be-done ?t ?d_t)
                                         (or
                                           (not (freshly_done ?d_t))
                                           (None ?d_t)
                                         )
                                         (done ?d_t)
                                    )
                                  )
                             )
                             (None ?t)
                         )
      )

      :effect (and (done ?t)

                   (freshly_done ?t)
                   (not (freshly_done ?p_t))

                   (prev_task ?t ?m)
                   (not (prev_task ?p_t ?m))

                   (prev_machine ?m)
                   (not (prev_machine ?p_m))

                   (increase (total-cost) 1)
              )


    )

)
