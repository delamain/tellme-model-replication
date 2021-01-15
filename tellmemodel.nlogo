; Developed for the EU funded TELL ME project (www.tellmeproject.eu) by the Centre for Research in
; Social Simulation, University of Surrey.

; Documentation is available from both the TELL ME and CRESS websites. The model requires the eXtraWidgets
; NetLogo extension to run.

extensions [gis profiler xw]
globals
[
  ; --------------------------
  ; INTERFACE
  
; BEHAVIOUR
  ; efficacy-vaccine         proportional reduction in risk to self and others if vaccinated
  ; efficacy-protect         proportional reduction in risk to self and others if non-vaccination behaviour adopted
  ; protectV-threshold       value (for attitude, norms and incidence combination) at which seek vaccination
  ; protectNV-threshold      value (for attitude, norms and incidence combination) to induce protective behaviour
; EPIDEMIOLOGY
  ; transmit-risk            probability of transmission over an SI pair for infection duration
  ; contactsPP               number of contacts per day a person makes
  ; latency-period           average period after exposure before infectious (days)
  ; recovery-period          average period of infection (days)
; OTHER
  ; country                  drop down box to select country specific information such as population counts
  ; prop-in-target           proportion of population in target group (high risk or other reason combined)
  ; popn-hcw                 healthcare workers per 1000 population
  ; prop-social-media        proportion of population who have access to social media
  
  ; --------------------------
  ; ADVANCED USER SETTINGS

  ;----- communication impact
  acceptance-range      ; (Extended GUI) size of latitude of acceptance for messages
  repeat-effect         ; (Extended GUI) relative effect of repeated message
  attitude-prop-M       ; (Extended GUI) proportionality constant for attitude change due to mass media messages
  attitude-prop-S       ; (Extended GUI) proportionality constant for attitude change due to social media messages
  attitude-prop-P       ; (Extended GUI) proportionality constant for attitude change due to messages in health publications
  attitude-prop-H       ; (Extended GUI) proportionality constant for attitude change due to messages provided by health profession
  flag-duration         ; (Extended GUI) number of ticks for heightened awareness of norms or recommendation
  antiV-threshold       ; threshold at which lower attitude is considered anti-vaccination
  standard-position     ; attitude value for general messages
  antivax-position      ; attitude value for messages targeted to anti-vaccination
  
  mass-media-prob       ; (Extended GUI) probability of responding to received mass media message
  social-media-prob     ; (Extended GUI) probability of responding to received social media message
  health-media-prob     ; (Extended GUI) probability of (hcw) responding to received health media message
  goto-hcw-prob         ; (Extended GUI) probability of talking to a healthcare worker
  normsV-bonus          ; (Extended GUI) additional norms influence for vaccination
  normsNV-bonus         ; (Extended GUI) additional norms influence for protective behaviour
  trust-bonus           ; (Extended GUI) increase to trust due to providing information
  attitude-decay        ; (Extended GUI) percent decay per tick to return to initial attitude if no further communication
  in-target-attitude    ; (Extended GUI) difference in initial attitude between those in/out target group

  ;----- behaviour model (NOTE: thresholds are provided by basic interface)
  see-distance          ; (Extended GUI) (Manhattan on patches) radius for proportion visibly infected
  incidence-discount    ; (Extended GUI) discount per timestep for epidemic history in risk calculations
  attitude-weight-V     ; (Extended GUI) coefficient of attitude in seeking vaccination
  norms-weight-V        ; (Extended GUI) coefficient of norms in seeking vaccination
  risk-weight-V         ; coefficient of risk in seeking vaccination
  attitude-weight-NV    ; (Extended GUI) coefficient of attitude in protective behaviour
  norms-weight-NV       ; (Extended GUI) coefficient of norms in protective behaviour
  risk-weight-NV        ; coefficient of risk in protective behaviour
  worry-relative        ; (Extended GUI) multiplier for threat perception compared to H1N1

  ;----- epidemic model (NOTE: SEIR transition rates are parameterised by basic interface)  
  travel-rate           ; (Extended GUI) proportion of contacts outside of patch
  travel-short          ; (Extended GUI) proportion of the contacts outside of patch that are with neighbouring patches
  when-declared         ; (Extended GUI) prevalence at which epidemic is considered to start
  
  ;----- policy context / scenarios
  isolate?                 ; whether isolation policy is part of scenario 
  si-effect-travel         ; proportion reduction in new cases arising from travel during quarantine
  si-effect-local          ; proportion reduction in infectivity within the patch during quarantine
  si-start-prev            ; prevalence at which quarantine takes effect
  si-duration              ; duration of quarantine
  isolate-flag?            ; whether isolation is included in scenario AND not yet occurred
  selfisolation-ticks      ; remaining duration of quarantine
  
  restrict-vaccine?        ; whether vaccines are delayed and/or eligibility
  vaccine-available        ; delay from epidemic declaration to vaccine availability
  vaccinate-who            ; population groups elgible for vaccine

  risk-misperceived?       ; whether risk is initially misperceived
  perceived-susceptibility ; believed value for discounted cumulative incidence
  risk-weighting           ; belived value for relative worry
  misperception-duration   ; number of days for which misperception continues (unless informed)
  
  frenzy?                  ; whether media frenzy at epidemic declaration stimulates behaviour
  frenzy-effect            ; population (%) that adopt behaviour regardless of attitude, norms, risk
  frenzy-memory            ; duration for which behaviour calculation ignored

  trust-lost?              ; whether there is an initial loss of trust
  trust-initial            ; average level of trust at initialisation
  trust-final              ; average level of trust that would be achieved without intervention  
  trust-restore            ; number of weeks (7 ticks) to get from trust-initial to trust-final

  ; --------------------------
  ; INTERNAL USE
  
  ; gis management
  popn-dataset          ; dataset to be imported
  GISenv                ; border of GIS dataset
  total-popn            ; to normalise patch populations
  max-popn              ; for colour scaling
  live-patches          ; the patchset over which the model is to run
  when-before           ; prevalence at which 'before' messages are created
  start-tick            ; tick at which epidemic met prevalence threshold and epidemic declared
  epidemic-declared?    ; flag to indicate whether epidemic has been declared
  start-si-tick         ; tick at which trigger prevalence reached for quarantine
  
  ; performance settings
  min-agents-per-patch  ; number of agents created in low population patches
  SEIR-beta             ; force of infection in epidemic model (excluding protective behaviour)
  SEIR-lambda           ; transition rate from E to I
  SEIR-gamma            ; transition rate from I to R
  start-epi-locations   ; number of patches where infections exist at start
  start-epi-population  ; average proportion of popn initially infected (in relevant locations)
  numPP-persons         ; (Extended GUI) drop down box to select number of agents per population on patch
  randomise?            ; (Extended GUI) whether to randomise or use random seed
  random-control        ; (Extended GUI) random seed used in simulation run, used only if randomise switch is off
;  num-messages          ; maximum number of messages in communications plan

  ; monitoring
  incidence             ; proportion of popn newly infected this tick
  max-incidence         ; maximum incidence during simulation
  when-max-incidence    ; tick at which maximum incidence
  prevalence            ; proportion of infected persions this tick
  max-prevalence        ; maximum prevalence during simulation
  when-max-prevalence   ; tick at which maximum prevalence
  prop-protect          ; proportion of people currently adopting protective behaviour
  max-protect           ; maximum proportion of people adopting protective behaviour
  when-max-protect      ; tick at which maximum protective
  prop-seek-vaccinate   ; proportion of people seeking vaccination (exceeding threshold)
  max-seek-vaccinate    ; maximum proportion of people seeing vaccination
  when-max-seek-vaccinate ; tick at which maximum vaccination sought
  prop-vaccinate        ; proportion of people seeking or previously adopted vaccination
  max-vaccinate         ; maximum proportion of people seeing or previously vaccination
  when-max-vaccinate    ; tick at which maximum vaccination starts (non decreasing)
    
]


breed [people person]   ; establish people as agents
people-own
[
  ; information access
  hcw?                  ; whether healthcare worker
  use-social-media?     ; whether user social media
  in-target?            ; whether in a target group
  
  ; attitudes and behaviour status
  attitudeV-initial     ; willingness to adopt vaccination based on demographic
  attitudeV-current     ; current willingness to adopt vaccination
  behaviourV-value      ; calculated value to compare to behaviour threshold
  behave-vaccinate?     ; whether seeks vaccination
  attitudeNV-initial    ; willingness to adopt non-vaccination behaviour based on demographic
  attitudeNV-current    ; current willingness to adopt non-vaccination behaviour
  behaviourNV-value     ; calculated value to compare to behaviour threshold
  behave-protect?       ; whether adopts other protective behaviour
  frenzied?             ; whether would adopt non-vaccination behaviour due to media frenzy
  
  ; effect of communication
  trust                 ; how much trusts communicator
  attitudeV-change      ; how much to adjust attitude
  attitudeNV-change     ; how much to adjust attitude
  info-received?        ; whether received information (trust and epidemic status)
  normsV-change         ; whether under influence of norms message
  normsNV-change        ; whether under influence of norms message
  rec-vaccinate         ; whether recommends behaviour type 'vaccinate'
  rec-protect           ; whether recommends behaviour type 'protect'

  ; disease progression
  exposed?              ; true means currently exposed but not yet infectious
  infected?             ; true means currently infected
  disease-day           ; days since exposed to infection
  immune?               ; true means recovered
  vaccinated?           ; true means successfully vaccinated
]

breed [ reps rep ]      ; one per patch to summarise the attitude behavior of people on that patch, for visualisation
reps-own
[
  ave-attitudeV
  max-attitudeV
  min-attitudeV  
  prop-vaccinate-patch  ; proportion of on-patch people seeking vaccination
  ave-attitudeNV
  max-attitudeNV
  min-attitudeNV  
  prop-protect-patch    ; proportion of on-patch people adopting protective behaviour
]

patches-own
[
  in-border?                   ; flag for whether patch is active in the model (ie not outside the country)
  popn                         ; population size
  ; epidemic model operations
  beta-local                   ; derived infectivity and contact parameter for SIR model
  new-cases-made               ; new infections created by infecteds on patch
  num-susceptible              ; size of population susceptible
  num-infected                 ; size of population infected
  num-exposed                  ; size of population exposed
  num-incidence                ; population to be converted to exposed
  num-travel-incases           ; new infection calculation variable - from travellers
  num-immune                   ; size of population immune (recovered)
  ; accessed by people on patch for behaviour
  visible-patches              ; neighbour patchset within specified distance (stored for efficiency)
  normsV                       ; proportion visible vaccination behaviour
  normsNV                      ; proportion visible protective behaviour
  cumulative-incidence         ; discounted incidence tracking for risk
  patch-risk                   ; calculated risk value over visible distance
  ; tracking
  first-infection              ; tick number for epidemic arrival
  prop-infected-now            ; proportion current exposed or infected
  prop-infected-ever           ; proportion ever exposed or infected
]

breed [ messages message ] ; media messages
messages-own
[
  trigger-value                ; prevalence at which triggered message activates or -1 for first death
  message-type                 ; B (before declaration), S (when declared), D (set day), R (regular)
                               ; A (after peak), N (national prevalence)
  ; characteristics of transmission
  media-channel                ; M (mass), S (social), P (health publications), H (health profession)
  when                         ; tick at which message occurs
  expiry                       ; number of ticks until message duration complete
  repeat?                      ; whether message part of series
  repeat-freq                  ; when replacement should be created
  relative-effect              ; reduces as same message repeated to implement familiarity
  ; content of message
  message-content              ; I (information), B (explain benefits), N (norms) or R (recommend)
  message-position             ; ideological position of message
  target-vaccination?          ; applies to vaccination
  target-protect?              ; applies to general protective behaviour
  target-group                 ; G (general), R (high risk), H (healthcare), I (infected), A (anti-vaccination)
  local?                       ; local (own patch only, prevalence trigger) or global effect
]  

; ---------------------------------------------------------------------------------
; MAIN LOOPS
; ---------------------------------------------------------------------------------

to startup
  setup-interface
  gui-defaults
end

to setup
  clear-all
  xwidgets-to-globals-all
  if randomise? [ set random-control new-seed
                  xw:set "random-control" random-control ]
  random-seed random-control
  setup-fixed-globals
  setup-country-specific
  setup-patch-variables
  setup-infection
  make-people
  make-reps
  setup-messages
  setup-frenzy
  color-patches
  reset-ticks
end

to go
  make-infections
  if sum [ num-incidence ] of live-patches < 1 [ stop ]       ; halt if no new exposures
  check-quarantine
  update-SEIR-patches
  update-SEIR-persons
  trigger-responsive-messages
  interpret-messages
  revise-trust
  revise-attitude
  revise-behaviour
  monitor-calculations
  if prevalence > when-declared and not epidemic-declared? [declare-epidemic]
  tick
end

to profile
  setup
  profiler:start
  repeat 10 [ go ]
  profiler:stop
  print profiler:report
  profiler:reset
end

; ---------------------------------------------------------------------------------
; INITIALISATION FUNCTIONS
; ---------------------------------------------------------------------------------


; --- COMMUNICATION

; create the set of messages from the input strategy
to setup-messages
  ; Each message input in the communication plan is individually checked. If marked "NONE" then skipped.
  ; Otherwise messages are created with appropriate 'when' values, or they are created as 'waiting' messages
  ; that will be activated as the trigger event occurs.

  let message-indices n-values num-messages [ (word "m" (? + 1)) ]
  foreach message-indices
  [ if xw:get (word ? "-trigger") != "NONE"
    [ make-my-messages (xw:get (word ? "-trigger")) (xw:get (word ? "-TPar"))
                       (xw:get (word ? "-channel")) (xw:get (word ? "-target"))
                       (xw:get (word ? "-content")) (xw:get (word ? "-behaviour"))
    ]
  ]
end

to make-my-messages [ my-trigger my-TPar my-channel my-target my-content my-behaviour ]
  let counter 1
  if my-trigger = "Before" [ set counter my-TPar ]         ; parameter is number of exposures for messages before epidemic
  create-messages counter
  [ hide-turtle
    set media-channel convert-channel (my-channel)
    set target-group convert-target (my-target)
    ifelse target-group != "A" [set message-position standard-position] [set message-position antivax-position]
    set message-content convert-content (my-content)
     
    ifelse my-behaviour = "Both" [ set target-vaccination? TRUE set target-protect? TRUE ]
    [ ifelse my-behaviour = "Vaccination" [ set target-vaccination? TRUE set target-protect? FALSE ]
                                          [ set target-vaccination? FALSE set target-protect? TRUE ]
    ]
      
    set repeat? FALSE
    set relative-effect 1
    set local? FALSE
      
    ifelse my-trigger = "Before" [ set message-type "B" set when -1 set trigger-value when-before ] [
    ifelse my-trigger = "Start"  [ set message-type "S" set when -1 set trigger-value 0 ] [
    ifelse my-trigger = "Day" [ set message-type "D" set when -1 set trigger-value my-TPar ] [
    ifelse my-trigger = "After Peak" [ set message-type "A" set when -1 set trigger-value my-TPar ] [
    ifelse my-trigger = "Regular" [ set message-type "R" set when -1 set repeat? TRUE
                                   set repeat-freq my-TPar ] [
    if my-trigger = "National Prevalence" [ set message-type "N" set when -1 set trigger-value my-TPar ]
    ] ] ] ] ]
  ]
end

to-report convert-target[ TG ]
  if TG = "All" [ report "G" ]
  if TG = "High risk" [ report "R" ]
  if TG = "Health workers" [ report "H" ]
  if TG = "Infected" [ report "I" ]
  if TG = "Anti-vaccination" [ report "A" ]
  type "ERROR: Invalid target group found: " print TG
end
  
to-report convert-channel[ CC ]
  if CC = "Mass media" [ report "M" ]
  if CC = "Social media" [ report "S" ]
  if CC = "Health media" [ report "P" ]
  if CC = "Health profession" [ report "H" ]
  type "ERROR: Invalid media channel found: " print CC
end

to-report convert-content [ CC ]
  if CC = "Epidemic Status" [ report "I" ]
  if CC = "Promote Benefits" [ report "B" ]
  if CC = "Emphasise Responsibility" [ report "N" ]
  if CC = "Recommend Adoption" [ report "R" ]
  type "ERROR: Invalid media content found: " print CC
end

;--- GLOBALS AND COUNTRY DATA

; set the values of globals not on the interface
to setup-fixed-globals

  ; coefficients for epidemic
  set SEIR-beta R0 / recovery-period
  ifelse latency-period = 0 [ set SEIR-lambda 0 ] [ set SEIR-lambda 1 / latency-period ] ; if 0, no E group
  set SEIR-gamma 1 / recovery-period
  set start-epi-locations 1
  set start-epi-population 0.001
  
  ; communication parameters
  set standard-position 0.9
  set antivax-position 0.3

  ; behaviour model parameters
  set risk-weight-V 1 - attitude-weight-V - norms-weight-V
  set risk-weight-NV 1 - attitude-weight-NV - norms-weight-NV

  ; operational parameters
  set min-agents-per-patch 10
  set when-before when-declared / 2
  ifelse isolate? [set isolate-flag? TRUE][set isolate-flag? FALSE]
  set epidemic-declared? FALSE
  set start-tick -1
  set start-si-tick 0
  set selfisolation-ticks 0
  
end

; import the population by patch information(GIS + miscellaneous)
to setup-country-specific
  load-country-data
  ; attach population density to patch
  set GISenv gis:envelope-of popn-dataset
  gis:set-world-envelope GISenv
  gis:apply-raster popn-dataset popn
  ; normalise to population count
  let factor 1000000 * total-popn / sum [popn] of patches with [ popn > 0 ]
  ask patches [ set popn round(popn * factor) ]
  ; set in-scope patches (note: after popn calculation is inefficient but ensures all outside are excluded)
  ask patches [ ifelse popn > 0 [ set in-border? TRUE ] [ set in-border? FALSE ] ]
  set live-patches patches with [ in-border? ]
  set max-popn max [ popn ] of live-patches + 1
end

;--- AGENTS AND PATCHES

; initialise patch variables
to setup-patch-variables
  ask live-patches
  [ set pcolor black
    if in-border?
    [ set visible-patches live-patches in-radius see-distance
      set num-susceptible popn
      set prop-infected-now 0
      set prop-infected-ever 0
      set cumulative-incidence 0
    ]
  ]
end

to setup-infection
  ask n-of start-epi-locations (max-n-of (start-epi-locations * 5) live-patches [popn])
  [ set num-infected random-float start-epi-population * popn
    if num-infected < 100 [set num-infected 100]
    set num-susceptible popn - num-infected
  ]
end

; create people agents, proportion vaccinated and random attitude
to make-people
  ask live-patches
  [ sprout-people max (list min-agents-per-patch (popn / numPP-persons))
    [ ; set fixed initial properties
      hide-turtle
      set exposed? false
      set infected? false
      set disease-day 0
      set immune? false
      set vaccinated? false
      set behave-protect? false
      set behave-vaccinate? false
      set frenzied? false
      
      ; media reception information
      ifelse random-float 1 < prop-in-target [set in-target? TRUE] [set in-target? FALSE]
      ifelse random-float 1 < popn-hcw / 1000 [set hcw? TRUE] [set hcw? FALSE]
      ifelse random-float 1 < prop-social-media [set use-social-media? TRUE] [set use-social-media? FALSE]

      initial-attitude             ; function call to set initial attitude
    ]
  ]
end

; triangular distribution with mode at 0.8 (so mean 0.6) for protect
; for vaccination, use 0.2 for antivaxxers and 0.8 for others
to initial-attitude
  ifelse random-float 1 < prop-antivax
    [ set attitudeV-initial triangular0to1 (0.125) (random-float 1) ]
    [ set attitudeV-initial triangular0to1 (0.75) (random-float 1) ]
  
  set attitudeNV-initial triangular0to1 (0.75) (random-float 1)
  
  ; adjust for in-target (ie risk or other target group) status
  ifelse in-target?
    [ set attitudeV-initial min ( list
        (attitudeV-initial + (1 - prop-in-target) * in-target-attitude) 1 )
      set attitudeNV-initial min ( list
        (attitudeNV-initial + (1 - prop-in-target) * in-target-attitude) 1 )
    ]
    [ set attitudeV-initial max ( list
        (attitudeV-initial - prop-in-target * in-target-attitude) 0 )
      set attitudeNV-initial max ( list
        (attitudeNV-initial - prop-in-target * in-target-attitude) 0 )
    ]

  ; set the 'current' values to the initial values
  set attitudeV-current attitudeV-initial
  set attitudeNV-current attitudeNV-initial

  ; set trust value
  ifelse trust-lost?
  [ set trust random-normal trust-initial 0.1
    if trust > 1 [ set trust 1]
    if trust < 0 [set trust 0 ]
  ]
  [ set trust 1 ]
end

; create reps - summary agents for people on patch
to make-reps
  ask live-patches
  [ sprout-reps 1
    [ set heading 0
      set size 0.5
      set shape "circle"
      set color white
      set ave-attitudeV mean [ attitudeV-current ] of people-here
      set min-attitudeV min [ attitudeV-current ] of people-here
      set max-attitudeV max [ attitudeV-current ] of people-here
      set prop-vaccinate-patch count people-here with [ behave-vaccinate? ] / count people-here
      set ave-attitudeV mean [ attitudeV-current ] of people-here
      set min-attitudeV min [ attitudeV-current ] of people-here
      set max-attitudeV max [ attitudeV-current ] of people-here
      set prop-protect-patch count people-here with [ behave-protect? ] / count people-here
    ]
  ]
end

;--- CONTEXT INITIALISATION

to setup-frenzy
  if frenzy?
  [ ask people
    [ if random-float 1 < frenzy-effect / 100
      [ set frenzied? TRUE]
    ]
  ]
end

; ---------------------------------------------------------------------------------
; SIMULATION FUNCTIONS
; ---------------------------------------------------------------------------------

to declare-epidemic
  set epidemic-declared? TRUE
  set start-tick ticks
  trigger-fixed-messages
end

; ---------------------------------------------------------------------------------
; Epidemic spread through patches
; ---------------------------------------------------------------------------------

; has quarantine prevalence trigger been reached and, if so, is quarantine still in effect?
to check-quarantine
  if isolate?
  [ ifelse selfisolation-ticks > 0
    [ set selfisolation-ticks selfisolation-ticks - 1 ]
    [ if prevalence > si-start-prev and isolate-flag?
      [ set selfisolation-ticks si-duration
        set isolate-flag? FALSE
        set start-si-tick ticks ]
    ]
  ]
end

; calculate the number of new exposures / infections and allocate to patches
to make-infections
  ; each patch calculates the number of new infections generated by itself, which are distributed as exposed
  ask live-patches
  [ set num-travel-incases 0               ; initialise taking of new cases assigned to patch
    
    ; calculate cases created by patch
    let PP max [ prop-protect-patch ] of reps-here    ; need to use 'max' as NetLogo cannot assume only one 'reps' agent is on patch
    let PV max [ prop-vaccinate-patch ] of reps-here
    set beta-local SEIR-beta * (1 - PP * efficacy-protect) * (1 - PV * efficacy-vaccine) ; adjust for protective behaviour and its efficacy
    if selfisolation-ticks > 0 [ set beta-local beta-local * (1 - si-effect-local) ]         ; adjust for quarantine (if in effect)
    set new-cases-made num-infected * beta-local * (num-susceptible / popn)       ; new infections
  ]

  ; each patch keeps some new infections, receives neighbours' close travellers and proportion of far travellers
  ; need to do all neighbour allocations before working out total new exposures
  ask live-patches
  [ let num-distribute new-cases-made * travel-rate * travel-short          ; number of new infections to distribute to neighbours
    if selfisolation-ticks > 0 [ set num-distribute num-distribute * (1 - si-effect-travel) ]  ; adjust for quarantine 
    let nbr-popn sum [ popn ] of neighbors with [ in-border? ]              ; total population of neigbhours
    ask neighbors with [ in-border? ]
    [ set num-travel-incases num-travel-incases + num-distribute * [ popn ] of self / nbr-popn   ; add the cases from close neighbours
    ]
  ]                 
  let migrate-infections travel-rate * (1 - travel-short) * sum [ new-cases-made ] of patches    ; allocation to long distance travellers
  
  ask live-patches
  [ ifelse selfisolation-ticks > 0                                              ; within patch infections
      [ set num-incidence new-cases-made * (1 - travel-rate) * (1 - si-effect-travel) ]
      [ set num-incidence new-cases-made * (1 - travel-rate) ]
    set num-incidence num-incidence                
      + migrate-infections * popn / sum [ popn ] of live-patches             ; from long distance travellers
      + num-travel-incases                                                   ; from short distance travellers
    if num-incidence > num-susceptible [ set num-incidence num-susceptible ] ; new infections cannot exceed susceptible population
  ]
end

to update-SEIR-patches
  ; incidence (new exposures) calculated in the make-infections procedure above
  ; calculate epidemic categories in reverse transmission order so not affected by incoming infections
  ask live-patches
  [ ; update epidemic compartment counts
    set num-immune num-immune + SEIR-gamma * num-infected                          ; prior to change in infected
    ifelse SEIR-lambda > 0                                                         ; SEIR model
    [ set num-infected (1 - SEIR-gamma) * num-infected + SEIR-lambda * num-exposed
      set num-exposed (1 - SEIR-lambda) * num-exposed + num-incidence
      if num-exposed < 1 [ set num-exposed 0 ]
    ]
    [ set num-infected (1 - SEIR-gamma) * num-infected + num-incidence             ; SIR (no E group)
      set num-exposed 0
      if num-infected < 1 [ set num-infected 0 ]
    ]
    set num-susceptible num-susceptible - num-incidence
    
    ; calculate discounted cumulative incidence
    set cumulative-incidence sum [num-incidence] of visible-patches / sum [popn] of visible-patches
        + (1 - incidence-discount) * cumulative-incidence
  ]
  color-patches
end

; ---------------------------------------------------------------------------------
; Epidemic applied to individuals - used for target of messages and monitoring
; ---------------------------------------------------------------------------------

to update-SEIR-persons
  ask people with [ infected? or exposed? ]
  [ ; for output, patterns of illness
    set disease-day disease-day + 1
    ; apply transition rates
    if SEIR-lambda > 0 and exposed?
    [ if random-float 1 < SEIR-lambda [ set exposed? FALSE
                                        set infected? TRUE ]
    ]
    if infected? and random-float 1 < SEIR-gamma
    [ set infected? FALSE
      set immune? TRUE
    ]
  ]
  
  ; new infections
  ask live-patches
  [ ask people-here with [ not exposed? and not infected? and not immune? and not vaccinated? ]
    [ if random-float 1 < num-incidence / popn
      [ ifelse SEIR-lambda > 0
        [ set exposed? TRUE ]
        [ set infected? TRUE ]
      ]
    ]
  ]
end

; ---------------------------------------------------------------------------------
;  Attitude change of individuals
; ---------------------------------------------------------------------------------

; activate messages that are triggered by epidemic conditions (prevalence, peak)
to trigger-responsive-messages
  ask messages with [message-type = "N" and when = -1]
  [ if prevalence > trigger-value [ set when ticks ]
  ]
  
  ask messages with [message-type = "A" and when = -1]
  [ if prevalence < trigger-value * max-prevalence [ set when ticks ]
  ]
end

; activate messages that occur on specific days after epidemic declared
to trigger-fixed-messages
  ask messages with [message-type = "S" or message-type = "D" or message-type = "R"]
  [ ifelse repeat?             ; my-TPar is frequency for repeat, and day for non-repeat
    [ set when ticks + 1 ]     ; adds 1 because epidemic declared at end of tick
    [ set when ticks + 1 + trigger-value ]
  ]
end


to interpret-messages
  ; reset the variables that hold the effect of communication this timestep
  ask people
  [ set attitudeV-change 0
    set attitudeNV-change 0
    set info-received? FALSE
    ; decrease remaining time of triggered flags
    if normsV-change > 0 [set normsV-change normsV-change - 1]
    if normsNV-change > 0 [set normsNV-change normsNV-change - 1]
    if rec-vaccinate > 0 [set rec-vaccinate rec-vaccinate - 1]
    if rec-protect > 0 [set rec-protect rec-protect - 1]
  ]
  
  ; apply the messages to set flags or store attitude change values
  ask messages with [ when = ticks ]                      ; select active messages
  ; check if person is in target group of message(s) and set flags for received
  [ if media-channel = "M"                                ; mass media - all exposed
    [ ask people
      [ if random-float 1 < mass-media-prob               ; exposed to message
           and check-target?  (myself) (self)             ; checks if in target group
           and ( not [local?] of myself or member? myself messages-here )
        [ respond-to-message (myself) (self) ]            ; calculates attitude change, sets message received flags
      ]
    ]
    if media-channel = "S"                                ; social media - subpopulation exposed
    [ ask people with [use-social-media?]
      [ if random-float 1 < social-media-prob             ; exposed to message
           and check-target?  (myself) (self)             ; checks if in target group
           and ( not [local?] of myself or member? myself messages-here )
        [ respond-to-message (myself) (self) ]            ; calculates attitude change, sets message received flags
      ]
    ]
    if media-channel = "P"                                ; health media - healthcare workers exposed
    [ ask people with [hcw?]
      [ if random-float 1 < health-media-prob             ; exposed to message
           and check-target?  (myself) (self)             ; checks if in target group
           and ( not [local?] of myself or member? myself messages-here )
        [ respond-to-message (myself) (self) ]            ; calculates attitude change, sets message received flags
      ]
    ]
    if media-channel = "H"                                ; discussion with healthcare workers - all exposed
    [ let relevant-attitude 0                             ; probability hcw passes on message is mean attitude
        ifelse [target-vaccination?] of self
        [ ifelse [target-protect?] of self
          [ set relevant-attitude max ( list (mean [attitudeV-current] of people with [hcw?])
                                             (mean [attitudeNV-current] of people with [hcw?]) ) ]
          [ set relevant-attitude mean [attitudeV-current] of people with [hcw?] ] ]
        [ set relevant-attitude mean [attitudeNV-current] of people with [hcw?] ]
       
      ask people
      [ if random-float 1 < goto-hcw-prob * relevant-attitude        ; exposed to message
           and check-target?  (myself) (self)             ; checks if in target group
           and ( not [local?] of myself or member? myself messages-here )
        [ respond-to-message (myself) (self) ]            ; calculates attitude change, sets message received flags
      ]
    ]
    
    ; message activity complete, create repeat or delete from plan    
    ifelse repeat?
      [ set when ticks + repeat-freq                      ; create next message for repeated
        set relative-effect relative-effect * repeat-effect    ; reduce effectiveness of next message
      ]
      [ die ]                                             ; delete completed message              

  ]
end
 
; called by interpret-message to check whether a message receiver is in target group
to-report check-target? [MM RR]      ; MM is message, RR is receiver
  let target-flag? FALSE
  if [target-group] of MM = "G"
     or ( [target-group] of MM = "R" and [in-target?] of RR )
     or ( [target-group] of MM = "H" and [hcw?] of RR )
     or ( [target-group] of MM = "I" and [infected?] of RR )
     or ( [target-group] of MM = "A" and [attitudeV-current] of RR < antiV-threshold )
    [ set target-flag? TRUE]
  report target-flag?
end

; called by interpret-message to select the appropriate attitude-proportion for the channel
to-report attitude-prop [MM]        ; MM is message
  if [media-channel] of MM = "M" [ report attitude-prop-M ]
  if [media-channel] of MM = "S" [ report attitude-prop-S ]
  if [media-channel] of MM = "P" [ report attitude-prop-P ]
  if [media-channel] of MM = "H" [ report attitude-prop-H ]
  type "ERROR: Invalid media channel found: " print [media-channel] of MM
end

; called by interpret-message to set flags that message has been received and its content
to respond-to-message [MM RR]      ; MM is message, RR is receiver
  
  ; set flag that information message is received
  if [message-content] of MM = "I" [ ask RR [set info-received? TRUE] ]
  
  ; for messages about vaccination
  if [target-vaccination?] of MM
    ; if message position is close enough, change (increase only) attitude
  [ if [message-content] of MM = "B"
       and [attitudeV-current] of RR > ( [message-position] of MM - acceptance-range )
       and [attitudeV-current] of RR < ( [message-position] of MM + acceptance-range )
       ; largest positive attitude change induced by all messages received in timestep
    [ ask RR
      [ set attitudeV-change max (list attitudeV-change
                  ( ([message-position] of MM - attitudeV-current)
                         * attitude-prop (MM) * [relative-effect] of MM * trust) )
      ]
    ]
    ; trigger / extend norms sensitivity flag
    if [message-content] of MM = "N" [ ask RR
      [ set normsV-change normsV-change + round ( [relative-effect] of MM * flag-duration) ] ]
    ; trigger / extend flag that received recommendation
    if [message-content] of MM = "R" [ ask RR
      [ set rec-vaccinate rec-vaccinate + round ( [relative-effect] of MM * flag-duration) ] ]
  ]

  ; for messages about protective behaviour
  if [target-protect?] of MM
    ; if message position is close enough, change (increase only) attitude
  [ if [message-content] of MM = "B"
       and [attitudeNV-current] of RR > ( [message-position] of MM - acceptance-range )
       and [attitudeNV-current] of RR < ( [message-position] of MM + acceptance-range )
       ; largest positive attitude change induced by all messages received in timestep
    [ ask RR
      [ set attitudeNV-change max (list attitudeNV-change 
                  ( ([message-position] of MM - attitudeNV-current)
                         * attitude-prop (MM) * [relative-effect] of MM * trust) ) ]
    ]
    ; trigger / extend norms sensitivity flag
    if [message-content] of MM = "N" [ ask RR
      [ set normsNV-change normsNV-change + round ( [relative-effect] of MM * flag-duration) ] ]
    ; trigger / extend flag that received recommendation
    if [message-content] of MM = "R" [ ask RR
      [ set rec-protect rec-protect + round ( [relative-effect] of MM * flag-duration) ] ]
  ]
end

to revise-trust
  ask people
  [ if epidemic-declared? and trust-lost? and ticks <= (start-tick + trust-restore * 7)
      [ set trust trust + (trust-final - trust-initial) / (trust-restore * 7) ]
    if info-received? [ set trust trust + trust-bonus
                        set info-received? FALSE ]
    if trust > 1 [set trust 1]
    if trust < 0 [set trust 0]      
  ]
end

to revise-attitude
  ask people
  [ set attitudeV-current (attitudeV-current + attitudeV-change)
    set attitudeV-current
      attitudeV-initial + (1 - attitude-decay / 100) * (attitudeV-current - attitudeV-initial)
    if attitudeV-current > 1 [set attitudeV-current 1]
    if attitudeV-current < 0 [set attitudeV-current 0]
    
    set attitudeNV-current (attitudeNV-current + attitudeNV-change)
    set attitudeNV-current
      attitudeNV-initial + (1 - attitude-decay / 100) * (attitudeNV-current - attitudeNV-initial)
    if attitudeNV-current > 1 [set attitudeNV-current 1]
    if attitudeNV-current < 0 [set attitudeNV-current 0]
  ]
  ask reps
  [ set ave-attitudeV mean [ attitudeV-current ] of people-here
    set min-attitudeV min [ attitudeV-current ] of people-here
    set max-attitudeV max [ attitudeV-current ] of people-here
    set ave-attitudeNV mean [ attitudeNV-current ] of people-here
    
    set min-attitudeNV min [ attitudeNV-current ] of people-here
    set max-attitudeNV max [ attitudeNV-current ] of people-here
  ]
end

; ---------------------------------------------------------------------------------
;  Behaviour of individuals
; ---------------------------------------------------------------------------------

; adopt protective behaviour if the behaviour value based on attitude and risk exceeds threshold
; and drop if below threshold
to revise-behaviour
  
  ; calculate norm (behave proportion) and risk at the patch level as same for all agents on patch
  ask live-patches
  [ let visible-people people-on visible-patches
    set normsV count visible-people with [ behave-vaccinate? ] / count visible-people
    set normsNV count visible-people with [ behave-protect? ] / count visible-people
    set patch-risk cumulative-incidence * worry-relative
  ]
  let max-risk max [patch-risk] of live-patches

  ask people
  [ ; identify whether real risk or maximum  real risk or mispereived risk is salient
    let salient-riskV get-risk (rec-vaccinate) (max-risk)
    let salient-riskNV get-risk (rec-protect) (max-risk)
        
    ; calculate behaviour values (weighted attitude, norms, worry, incidence)
    set behaviourV-value attitude-weight-V * attitudeV-current
                         + norms-weight-V * [normsV] of patch-here
                         + risk-weight-V * salient-riskV
    set behaviourNV-value attitude-weight-NV * attitudeNV-current
                          + norms-weight-NV * [normsNV] of patch-here
                          + risk-weight-NV * salient-riskNV

    if normsV-change > 0                    ; check if norms message in effect
      [ set behaviourV-value behaviourV-value + norms-weight-V * normsV-bonus ]
    if normsNV-change > 0                    ; check if norms message in effect
      [ set behaviourNV-value behaviourNV-value + norms-weight-NV * normsNV-bonus ]

    ; compare calculated behaviour values to thresholds for adoption
      ; for vaccination, can adopt or drop intent until vaccine is available, then only adopt
    if not behave-vaccinate? and behaviourV-value > protectV-threshold
      [ seek-vaccination ]
      ; for non-vaccination, can adopt or drop behaviour as desired
    ifelse behave-protect?            ; set up to allow different adopt and drop thresholds
      [ if behaviourNV-value < protectNV-threshold [set behave-protect? FALSE] ]
      [ if behaviourNV-value > protectNV-threshold [set behave-protect? TRUE] ]
      
    ; implement media frenzy non-vaccination response
    if frenzied?
    [ set behave-protect? TRUE
      if random-float 1 < 1 / (frenzy-memory * 30.4) [ set frenzied? FALSE ]
    ]
  ]
  
  ; monitoring and visualisation
  ask reps [ set prop-protect-patch count people-here with [ behave-protect? ] / count people-here ]
  ask reps [ set prop-vaccinate-patch count people-here with [ behave-vaccinate? ] / count people-here ]
  color-reps
end

to seek-vaccination
  if not restrict-vaccine? or                                                           ; does vaccination context apply
   (epidemic-declared? and ticks >= start-tick + vaccine-available and v-eligible?)     ; does a vaccine exist?
    [ set behave-vaccinate? TRUE
      if random-float 1 < efficacy-vaccine [ set vaccinated? TRUE ]
    ]
end

; returns the salient risk value based on whether currently misperceived and whether recommended behaviour
to-report get-risk [RR MR]     ; RR is whether recommendation current, MR is max-risk
  if not risk-misperceived?
     or ( epidemic-declared? and ( ticks > start-tick + misperception-duration ) )
     or info-received?
     [ ifelse RR > 0
       [ report MR ]
       [ report [patch-risk] of patch-here ]
     ]
       
  report perceived-susceptibility * risk-weighting
end

to-report v-eligible?
  if member? "All" xw:get "vaccinate-who" [report TRUE]
  if member? "Target group" xw:get "vaccinate-who" and in-target? [report TRUE]
  if member? "Healthcare workers" xw:get "vaccinate-who" and hcw? [report TRUE]
  report FALSE
end
 

; ---------------------------------------------------------------------------------
; DATA AND CHARTS
; ---------------------------------------------------------------------------------

to monitor-calculations
  set incidence sum [ num-incidence ] of live-patches / sum [ popn ] of live-patches
  if incidence > max-incidence
  [ set max-incidence incidence
    set when-max-incidence ticks
  ]
  set prevalence sum [ num-infected ] of live-patches / sum [ popn ] of live-patches
  if prevalence > max-prevalence
  [ set max-prevalence prevalence
    set when-max-prevalence ticks
  ]
  set prop-protect count people with [behave-protect?] / count people
  if prop-protect > max-protect
  [ set max-protect prop-protect
    set when-max-protect ticks
  ]
  set prop-seek-vaccinate count people with [behaviourV-value > protectV-threshold] / count people
  if prop-seek-vaccinate > max-seek-vaccinate
  [ set max-seek-vaccinate prop-seek-vaccinate
    set when-max-seek-vaccinate ticks
  ]
  set prop-vaccinate count people with [behave-vaccinate?] / count people
  if prop-vaccinate > max-vaccinate
  [ set max-vaccinate prop-vaccinate
    set when-max-vaccinate ticks
  ]
end

; Epidemic progression and impact
;  plot of prevalence and incidence and secondary infections over time
;  eg plot count people with [ disease-day = 0 and infected? ] / count people
;  monitor of number of people infected by those currently infected and not newly infected
;  monitors for maximum prevalence / incidence and when they occurred

; ---------------------------------------------------------------------------------
; UTILITY FUNCTIONS
; ---------------------------------------------------------------------------------

;--- CONNECT global variables and extended widgets

; set the globals from the widgets on extended gui
to xwidgets-to-globals-all
  xw:ask xw:widgets xw:with [ xw:kind != "NOTE" and xw:tab != "comms" ]
  [ run (word "set " xw:key " " format xw:get xw:key)
  ]      
end

to-report format [ value ]
  report ifelse-value is-string? value
    [ (word "\"" value "\"") ]
    [ ifelse-value is-list? value
      [ reduce word (sentence "[" (map format value) "]") ]
      [ value ]
    ]
end

; takes a list of xwidget names and sets the same-name global variables to the value
to transfer-xw-to-globals [xw-list]      ; xw-list is names of xwidgets in quotes
  foreach xw-list [ run ( word "set " ? " xw:get " "\"" ? "\"")]
end

; takes a list of global variables and sets the same-name xwidgets to the value
to transfer-globals-to-xw [var-list]     ; var-list is names of global variables in quotes
  foreach var-list [ run ( word "xw:set " "\"" ? "\" " ? )]
end

;--- OTHER calculations and colouring

to-report triangular0to1 [ MM UU ]
  ; from a random UU uniform [0,1], converts to triangular distribution with mode MM
  ifelse UU < MM
   [ report sqrt ( UU * MM ) ]
   [ report 1 - sqrt ( (1 - UU) * (1 - MM) ) ]
end

to color-patches
  ask live-patches
  [ ifelse num-infected > 0.03 * popn [ set pcolor 16 ] [
    ifelse num-infected >= 1 [ set pcolor 18 ] [
    ifelse num-immune < num-susceptible
      [ ifelse popn < 0.01 * max-popn [ set pcolor [ 200 200 255 ] ] [
        ifelse popn < 0.05 * max-popn [ set pcolor [ 160 160 255 ] ] [           
        ifelse popn < 0.20 * max-popn [ set pcolor [ 120 120 220 ] ] [           
        ifelse popn < 0.80 * max-popn [ set pcolor [ 060 060 220 ] ] [           
        ifelse popn < 1.00 * max-popn [ set pcolor [ 000 000 220 ] ] [
      ]]]]]]          
      [ ifelse popn < 0.01 * max-popn [ set pcolor [ 200 255 200 ] ] [
        ifelse popn < 0.05 * max-popn [ set pcolor [ 160 255 160 ] ] [           
        ifelse popn < 0.20 * max-popn [ set pcolor [ 120 220 120 ] ] [           
        ifelse popn < 0.80 * max-popn [ set pcolor [ 060 220 060 ] ] [
        ifelse popn < 1.00 * max-popn [ set pcolor [ 000 220 000 ] ] [
      ]]]]]]          
    ]]
  ]
end

to color-reps
  ask reps
  [ ifelse (prop-protect-patch + prop-vaccinate-patch) > 1
      [ set color violet - 2 ]
      [ set color white ]
  ]
end

; ---------------------------------------------------------------------------------
; DEFAULT values
; ---------------------------------------------------------------------------------

; set all context switches to off and assocaiated variables to non-effect values
to clear-contexts
  ; quarantine
  set isolate? FALSE
  set si-effect-travel 0
  set si-effect-local 0
  set si-start-prev when-declared
  set si-duration 0
  transfer-globals-to-xw (list "isolate?" "si-effect-travel" "si-effect-local"
                          "si-start-prev" "si-duration")
  ; media frenzy
  set frenzy? FALSE
  set frenzy-effect 0
  set frenzy-memory 1
  transfer-globals-to-xw (list "frenzy?" "frenzy-effect" "frenzy-memory")
  ; loss of trust
  set trust-lost? FALSE
  set trust-initial 1
  set trust-final 1
  set trust-restore 1
  transfer-globals-to-xw (list "trust-lost?" "trust-initial" "trust-final"
                          "trust-restore")
  ; vaccine restrictions
  set restrict-vaccine? FALSE
  set vaccine-available 0
  set vaccinate-who (list "All")
  transfer-globals-to-xw (list "restrict-vaccine?" "vaccine-available")
  xw:set "vaccinate-who" (list "All")
  ; risk misperception
  set risk-misperceived? FALSE
  set perceived-susceptibility 0
  set risk-weighting 1
  set misperception-duration 0
  transfer-globals-to-xw (list "risk-misperceived?" "perceived-susceptibility"
                          "risk-weighting" "misperception-duration")
end

; default values for behaviour
to default-behaviour
  set see-distance 3
  set prop-social-media 0.7
  set prop-in-target 0.1
  set popn-hcw 10
  
  set incidence-discount 0.14
  set worry-relative 1
  set attitude-weight-V 0.3
  set norms-weight-V 0.15
  set protectV-threshold 0.3
  set attitude-weight-NV 0.35
  set norms-weight-NV 0.1
  set protectNV-threshold 0.25
  
  set efficacy-vaccine 0.7
  set efficacy-protect 0.25
  
  set prop-antivax 0.1
  set in-target-attitude 0.1

  transfer-globals-to-xw (list "see-distance" "incidence-discount" "worry-relative"
                          "attitude-weight-V" "norms-weight-V" "attitude-weight-NV"
                          "norms-weight-NV" "in-target-attitude")
end

; set the default values for all the extended widgets (together so easier to find and change)
to gui-defaults
  
  ; policy context
  xw:set "isolate?" FALSE
  xw:set "si-effect-travel" 0
  xw:set "si-effect-local" 0
  xw:set "si-start-prev" 0.001
  xw:set "si-duration" 0
  xw:set "restrict-vaccine?" FALSE
  xw:set "vaccine-available" 0
  xw:set "vaccinate-who" (list "All")
  xw:set "risk-misperceived?" FALSE
  xw:set "perceived-susceptibility" 0
  xw:set "risk-weighting" 1
  xw:set "misperception-duration" 0
  xw:set "frenzy?" FALSE
  xw:set "frenzy-effect" 0
  xw:set "frenzy-memory" 1
  xw:set "trust-lost?" FALSE
  xw:set "trust-initial" 1
  xw:set "trust-final" 1
  xw:set "trust-restore" 1

  ; advanced parameters  
  xw:set "travel-rate" 0.25
  xw:set "travel-short" 0.6
  xw:set "when-declared" 0.001
  xw:set "see-distance" 3
  xw:set "numPP-persons" 5000
  xw:set "randomise?" TRUE
  xw:set "random-control" 0
  xw:set "in-target-attitude" 0.1
  xw:set "attitude-decay" 2
  xw:set "mass-media-prob" 0.95
  xw:set "social-media-prob" 0.60
  xw:set "health-media-prob" 0.80
  xw:set "goto-hcw-prob" 0.10
  xw:set "acceptance-range" 0.4
  xw:set "repeat-effect" 0.9
  xw:set "attitude-prop-M" 0.05
  xw:set "attitude-prop-S" 0.1
  xw:set "attitude-prop-P" 0.2
  xw:set "attitude-prop-H" 0.3
  xw:set "trust-bonus" 0.05
  xw:set "flag-duration" 5
  xw:set "normsV-bonus" 0.2
  xw:set "normsNV-bonus" 0.4
  xw:set "incidence-discount" 0.14
  xw:set "worry-relative" 1
  xw:set "attitude-weight-V" 0.3
  xw:set "norms-weight-V" 0.15
  xw:set "attitude-weight-NV" 0.35
  xw:set "norms-weight-NV" 0.1
end

to load-country-data
  ; load the correct GIS population density and country specific travel values
  if country = "Austria" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Austria 2015.asc"
    set total-popn 8.6 ]
  if country = "Belgium" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Belgium 2015.asc"
    set total-popn 11.2 ]
  if country = "Bulgaria" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Bulgaria 2015.asc"
    set total-popn 7.1 ]
  if country = "Croatia" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Croatia 2015.asc"
    set total-popn 4.26 ]
  if country = "Cyprus" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Cyprus 2015.asc"
    set total-popn 1.16 ]
  if country = "Czech Republic" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Czech Republic 2015.asc"
    set total-popn 10.8 ]
  if country = "Denmark" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Denmark 2015.asc"
    set total-popn 5.7 ]
  if country = "Estonia" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Estonia 2015.asc"
    set total-popn 1.3 ]
  if country = "Finland" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Finland 2015.asc"
    set total-popn 5.46 ]
  if country = "France" [
    set popn-dataset gis:load-dataset "GISdata/Popn density France 2015.asc"
    set total-popn 65 ]
  if country = "Germany" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Germany 2015.asc"
    set total-popn 82.6 ]
  if country = "Greece" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Greece 2015.asc"
    set total-popn 11.1 ]
  if country = "Hungary" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Hungary 2015.asc"
    set total-popn 9.9 ]
  if country = "Ireland" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Ireland 2015.asc"
    set total-popn 4.73 ]
  if country = "Italy" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Italy 2015.asc"
    set total-popn 61 ]
  if country = "Latvia" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Latvia 2015.asc"
    set total-popn 2 ]
  if country = "Lithuania" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Lithuania 2015.asc"
    set total-popn 3 ]
  if country = "Luxembourg" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Luxembourg 2015.asc"
    set total-popn 0.54 ]
  if country = "Malta" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Malta 2015.asc"
    set total-popn 0.43 ]
  if country = "Netherlands" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Netherlands 2015.asc"
    set total-popn 16.8 ]
  if country = "Poland" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Poland 2015.asc"
    set total-popn 38 ]
  if country = "Portugal" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Portugal 2015.asc"
    set total-popn 10.6 ]
  if country = "Romania" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Romania 2015.asc"
    set total-popn 21.6 ]
  if country = "Slovakia" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Slovakia 2015.asc"
    set total-popn 5.5 ]
  if country = "Slovenia" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Slovenia 2015.asc"
    set total-popn 2.1 ]
  if country = "Spain" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Spain 2015.asc"
    set total-popn 47 ]
  if country = "Sweden" [
    set popn-dataset gis:load-dataset "GISdata/Popn density Sweden 2015.asc"
    set total-popn 9.7 ]
  if country = "United Kingdom" [
    set popn-dataset gis:load-dataset "GISdata/Popn density UK 2015.asc"
    set total-popn 64 ]
end

; ---------------------------------------------------------------------------------
; PRESET SCENARIOS
; ---------------------------------------------------------------------------------

; called by epidemic scenarios weak flu button
to scenario-E1
  set R0 1.4
  set latency-period 2
  set recovery-period 5
end

; called by epidemic scenarios strong flu button
to scenario-E2
  set R0 2
  set latency-period 1
  set recovery-period 5
end

; called by epidemic scenarios extreme button
to scenario-E3
  set R0 6
  set latency-period 7
  set recovery-period 20
end

; called by communications scenarios low button
to scenario-C1
  set num-messages 6
  xw:remove "comms"
  setup-gui-comms
  xw:set "m1-trigger" "Before" xw:set "m1-TPar" 0 xw:set "m1-channel" "Mass media" xw:set "m1-target" "High risk"
    xw:set "m1-content" "Recommend Adoption" xw:set "m1-behaviour" "Both"
  xw:set "m2-trigger" "Before" xw:set "m2-TPar" 0 xw:set "m2-channel" "Social media" xw:set "m2-target" "High risk"
    xw:set "m2-content" "Recommend Adoption" xw:set "m2-behaviour" "Both"
  xw:set "m3-trigger" "Before" xw:set "m3-TPar" 0 xw:set "m3-channel" "Health media" xw:set "m3-target" "Health workers"
    xw:set "m3-content" "Promote Benefits" xw:set "m3-behaviour" "Both"
  xw:set "m4-trigger" "Before" xw:set "m4-TPar" 0 xw:set "m4-channel" "Health profession" xw:set "m4-target" "Infected"
    xw:set "m4-content" "Promote Benefits" xw:set "m4-behaviour" "Other Protective"
  xw:set "m5-trigger" "Regular" xw:set "m5-TPar" 3 xw:set "m5-channel" "Mass media" xw:set "m5-target" "All"
    xw:set "m5-content" "Epidemic Status" xw:set "m5-behaviour" "Both"
  xw:set "m6-trigger" "After Peak" xw:set "m6-TPar" 0.5 xw:set "m6-channel" "Health profession" xw:set "m6-target" "High risk"
    xw:set "m6-content" "Recommend Adoption" xw:set "m6-behaviour" "Other Protective"
end

; called by communications scenarios medium button
to scenario-C2
  set num-messages 9
  xw:remove "comms"
  setup-gui-comms
  xw:set "m1-trigger" "Day" xw:set "m1-TPar" 1 xw:set "m1-channel" "Mass media" xw:set "m1-target" "All"
    xw:set "m1-content" "Promote Benefits" xw:set "m1-behaviour" "Other Protective"
  xw:set "m2-trigger" "Day" xw:set "m2-TPar" 1 xw:set "m2-channel" "Mass media" xw:set "m2-target" "All"
    xw:set "m2-content" "Recommend Adoption" xw:set "m2-behaviour" "Other Protective"
  xw:set "m3-trigger" "Regular" xw:set "m3-TPar" 3 xw:set "m3-channel" "Health profession" xw:set "m3-target" "High risk"
    xw:set "m3-content" "Promote Benefits" xw:set "m3-behaviour" "Both"
  xw:set "m4-trigger" "Regular" xw:set "m4-TPar" 3 xw:set "m4-channel" "Health profession" xw:set "m4-target" "High risk"
    xw:set "m4-content" "Epidemic status" xw:set "m4-behaviour" "Other Protective"
  xw:set "m5-trigger" "Regular" xw:set "m5-TPar" 3 xw:set "m5-channel" "Mass media" xw:set "m5-target" "All"
    xw:set "m5-content" "Epidemic Status" xw:set "m5-behaviour" "Both"
  xw:set "m6-trigger" "Regular" xw:set "m6-TPar" 3 xw:set "m6-channel" "Social media" xw:set "m6-target" "All"
    xw:set "m6-content" "Epidemic Status" xw:set "m6-behaviour" "Both"
  xw:set "m7-trigger" "After Peak" xw:set "m7-TPar" 0.5 xw:set "m7-channel" "Mass media" xw:set "m7-target" "All"
    xw:set "m7-content" "Epidemic status" xw:set "m7-behaviour" "Both"
  xw:set "m8-trigger" "After Peak" xw:set "m8-TPar" 0.5 xw:set "m8-channel" "Health profession" xw:set "m8-target" "Infected"
    xw:set "m8-content" "Recommend Adoption" xw:set "m8-behaviour" "Other Protective"
  xw:set "m9-trigger" "After Peak" xw:set "m9-TPar" 0.5 xw:set "m9-channel" "Social media" xw:set "m9-target" "All"
    xw:set "m9-content" "Promote Benefits" xw:set "m9-behaviour" "Both"
end

; called by communications scenarios high button
to scenario-C3
  set num-messages 10
  xw:remove "comms"
  setup-gui-comms
  xw:set "m1-trigger" "Before" xw:set "m1-TPar" 0 xw:set "m1-channel" "Mass media" xw:set "m1-target" "High risk"
    xw:set "m1-content" "Recommend Adoption" xw:set "m1-behaviour" "Other Protective"
  xw:set "m2-trigger" "Before" xw:set "m2-TPar" 0 xw:set "m2-channel" "Social media" xw:set "m2-target" "High risk"
    xw:set "m2-content" "Recommend Adoption" xw:set "m2-behaviour" "Other Protective"
  xw:set "m3-trigger" "Before" xw:set "m3-TPar" 0 xw:set "m3-channel" "Health media" xw:set "m3-target" "Health workers"
    xw:set "m3-content" "Promote Benefits" xw:set "m3-behaviour" "Other Protective"
  xw:set "m4-trigger" "Day" xw:set "m4-TPar" 20 xw:set "m4-channel" "Mass media" xw:set "m4-target" "All"
    xw:set "m4-content" "Epidemic Status" xw:set "m4-behaviour" "Other Protective"
  xw:set "m5-trigger" "Day" xw:set "m5-TPar" 20 xw:set "m5-channel" "Mass media" xw:set "m5-target" "All"
    xw:set "m5-content" "Promote Benefits" xw:set "m5-behaviour" "Other Protective"
  xw:set "m6-trigger" "National Prevalence" xw:set "m6-TPar" 0.01 xw:set "m6-channel" "Mass media" xw:set "m6-target" "All"
    xw:set "m6-content" "Promote Benefits" xw:set "m6-behaviour" "Other Protective"
  xw:set "m7-trigger" "Regular" xw:set "m7-TPar" 3 xw:set "m7-channel" "Mass media" xw:set "m7-target" "All"
    xw:set "m7-content" "Epidemic Status" xw:set "m7-behaviour" "Other Protective"
  xw:set "m8-trigger" "Regular" xw:set "m8-TPar" 3 xw:set "m8-channel" "Social media" xw:set "m8-target" "All"
    xw:set "m8-content" "Epidemic Status" xw:set "m8-behaviour" "Other Protective"
  xw:set "m9-trigger" "After Peak" xw:set "m9-TPar" 0.5 xw:set "m9-channel" "Mass media" xw:set "m9-target" "All"
    xw:set "m9-content" "Promote Benefits" xw:set "m9-behaviour" "Other Protective"
  xw:set "m10-trigger" "After Peak" xw:set "m10-TPar" 0.5 xw:set "m10-channel" "Health profession" xw:set "m10-target" "High risk"
    xw:set "m10-content" "Recommend Adoption" xw:set "m10-behaviour" "Other Protective"
end


; ---------------------------------------------------------------------------------
; INTERFACE construction
; ---------------------------------------------------------------------------------

; construct the tabs and widgets except for communication plan
to setup-interface
  xw:clear-all
  setup-gui-comms
  setup-gui-context
  setup-gui-advpar
end  

;--- Communication plan tab
to setup-gui-comms
  
  ; headings
  xw:create-tab "comms"
  [ xw:set-order 1
    xw:set-title "Communications Plan"
  ]
  xw:create-note "comms-h1"
  [ xw:set-text "Trigger"
    xw:set-x 10
    xw:set-y 5
    xw:set-width 250
  ]
  xw:create-note "comms-h2"
  [ xw:set-text "Delivery"
    xw:set-x 290
    xw:set-y 5
    xw:set-width 300
  ]
  xw:create-note "comms-h3"
  [ xw:set-text "Message Content"
    xw:set-x 620
    xw:set-y 5
    xw:set-width 350
  ]
  
  ; creates X sets of message parameters where X is given by global variable num-messages 
  let message-indices n-values num-messages [ (word "m" (? + 1)) ]
  foreach message-indices
  [ xw:create-chooser ( word ? "-trigger" )
    [ xw:set-label ( word "Trigger (" ? ")" )
      xw:set-x 10
      xw:set-y 60 * (position ? message-indices) + 40
      xw:set-width 150
      xw:set-items [ "NONE" "Before" "Start" "Day" "Regular" "After Peak" "National Prevalence" ]
    ]
    
    xw:create-numeric-input ( word ? "-TPar" )
    [ xw:set-label ( word "Day / Level (" ? ")" )
      xw:set-x 160
      xw:set-y 60 * (position ? message-indices) + 40
      xw:set-width 100
    ]
    
    xw:create-chooser ( word ? "-target" )
    [ xw:set-label ( word "Target group (" ? ")" )
      xw:set-x 290
      xw:set-y 60 * (position ? message-indices) + 40
      xw:set-width 150
      xw:set-items [ "All" "High risk" "Health workers" "Infected" "Anti-vaccination" ]
    ]

    xw:create-chooser ( word ? "-channel" )
    [ xw:set-label ( word "Media channel (" ? ")" )
      xw:set-x 440
      xw:set-y 60 * (position ? message-indices) + 40
      xw:set-width 150
      xw:set-items [ "Mass media" "Social media" "Health media" "Health profession" ]
    ]
    
    xw:create-chooser ( word ? "-content" )
    [ xw:set-label ( word "Content (" ? ")" )
      xw:set-x 620
      xw:set-y 60 * (position ? message-indices) + 40
      xw:set-width 200
      xw:set-items [ "Epidemic Status" "Promote Benefits" "Emphasise Responsibility" "Recommend Adoption" ]
    ]
      
    xw:create-chooser ( word ? "-behaviour" )
    [ xw:set-label ( word "Behaviour type (" ? ")" )
      xw:set-x 820
      xw:set-y 60 * (position ? message-indices) + 40
      xw:set-width 150
      xw:set-items [ "Both" "Vaccination" "Other Protective" ]
    ]
      
  ]
  
  xw:ask "comms" [ xw:set-color white ]
  xw:ask xw:widgets xw:with [xw:tab = "comms" and xw:kind != "NOTE"] [ xw:set-color blue + 3 ]
  xw:ask xw:notes xw:with [xw:tab = "comms"] [ xw:set-color blue - 1
                                               xw:set-font-color white
                                               xw:set-opaque? TRUE ]
 
end
        
 
;--- Policy Context (Scenarios)
to setup-gui-context

  xw:create-tab "context"
  [ xw:set-order 2
    xw:set-title "Policy Context"
  ]
  
  ; self-isolation (quarantine)
  xw:create-note "context-h1"
  [ xw:set-text "Encourage voluntary (or compulsory) self-isolation of those infected"
    xw:set-x 10
    xw:set-y 5
  ]
  
  xw:create-checkbox "isolate?"
  [ xw:set-label "Isolation?"
    xw:set-y 31
  ]
  
  xw:create-slider "si-effect-travel"
  [ xw:set-label "Reduction in travel (proportion)"
    xw:set-y 31
    xw:set-increment 0.01
    xw:set-maximum 1
  ]

  xw:create-slider "si-effect-local"
  [ xw:set-label "Reduction in local contacts (proportion)"
    xw:set-y 81
    xw:set-increment 0.01
    xw:set-maximum 1
  ]
  
  xw:create-numeric-input "si-start-prev"
  [ xw:set-label "Triggering prevalence"
    xw:set-y 31
  ]
  
  xw:create-slider "si-duration"
  [ xw:set-label "Duration of policy"
    xw:set-y 81
    xw:set-minimum 0
    xw:set-increment 1
    xw:set-maximum 100
    xw:set-units "days"
  ]
  
  ; Restricted access to vaccine
  xw:create-note "context-h2"
  [ xw:set-text "Restrictions on access to vaccine (delay or eligibility)"
    xw:set-x 10
    xw:set-y 151
  ]

  xw:create-checkbox "restrict-vaccine?"
  [ xw:set-label "Restrictions on vaccine?"
    xw:set-y 177
  ]
  
  xw:create-slider "vaccine-available"
  [ xw:set-label "Delay before available"
    xw:set-y 177
    xw:set-increment 1
    xw:set-maximum 100
    xw:set-units "days"
  ]
  
  xw:create-multi-chooser "vaccinate-who"
  [ xw:set-label "Eligible population"
    xw:set-y 177
    xw:set-height 90
    xw:set-items (list "All" "Target group" "Healthcare workers")
  ]

  ; misperception of risk
  xw:create-note "context-h3"
  [ xw:set-text "Misperception of risk: prevalence and threat"
    xw:set-x 10
    xw:set-y 287
  ]
  
  xw:create-checkbox "risk-misperceived?"
  [ xw:set-label "Risk misperceived?"
    xw:set-y 313
  ]
  
  xw:create-slider "perceived-susceptibility"
  [ xw:set-label "Perceived risk of infection"
    xw:set-y 313
    xw:set-increment 0.01
    xw:set-maximum 1
  ]

  xw:create-slider "risk-weighting"
  [ xw:set-label "Perceived severity (1 = H1N1)"
    xw:set-y 363
    xw:set-minimum 1
    xw:set-increment 1
    xw:set-maximum 5
  ]
  
  xw:create-slider "misperception-duration"
  [ xw:set-label "Duration of misperception"
    xw:set-y 313
    xw:set-increment 1
    xw:set-maximum 100
    xw:set-units "days"
  ]
  
  ; media frenzy
  xw:create-note "context-h4"
  [ xw:set-text "Media frenzy increases initial protective behaviour"
    xw:set-x 10
    xw:set-y 433
  ]
  
  xw:create-checkbox "frenzy?"
  [ xw:set-label "Frenzy occurs?"
    xw:set-y 459
  ]
  
  xw:create-slider "frenzy-effect"
  [ xw:set-label "Adopt nonvaccination behaviour"
    xw:set-y 459
    xw:set-increment 1
    xw:set-maximum 100
    xw:set-units "%"
  ]

  xw:create-slider "frenzy-memory"
  [ xw:set-label "Duration of media frenzy effect"
    xw:set-y 459
    xw:set-minimum 1
    xw:set-increment 1
    xw:set-maximum 12
    xw:set-units "months"
  ]

  ; loss of trust in health authority communications
  xw:create-note "context-h5"
  [ xw:set-text "Loss of trust in health communication"
    xw:set-x 10
    xw:set-y 529
  ]
  
  xw:create-checkbox "trust-lost?"
  [ xw:set-label "Trust lost?"
    xw:set-y 555
  ]
  
  xw:create-slider "trust-initial"
  [ xw:set-label "Average trust at start of epidemic"
    xw:set-y 555
    xw:set-increment 0.01
    xw:set-maximum 1
  ]

  xw:create-slider "trust-final"
  [ xw:set-label "Trust level once recovered"
    xw:set-y 605
    xw:set-increment 0.01
    xw:set-maximum 1
  ]
  
  xw:create-slider "trust-restore"
  [ xw:set-label "Recovery period for trust"
    xw:set-y 555
    xw:set-minimum 1
    xw:set-increment 1
    xw:set-maximum 30
    xw:set-units "weeks"
  ]
  
  ; Formatting
  
  xw:ask xw:notes xw:with [xw:tab = "context"]
         [ xw:set-width 770
         ]
         
  xw:ask xw:checkboxes xw:with [xw:tab = "context"]
         [ xw:set-x 10
           xw:set-width 150
         ]
         
  xw:ask [ "si-effect-travel" "si-effect-local" "vaccine-available" "vaccinate-who"
           "perceived-susceptibility" "risk-weighting" "frenzy-effect"
           "trust-initial" "trust-final"]
         [ xw:set-x 170
           xw:set-width 300
         ]

  xw:ask [ "si-start-prev" "si-duration" "vaccine-available"
           "misperception-duration" "frenzy-memory" "trust-restore"]
         [ xw:set-x 480
           xw:set-width 300
         ]
         
  xw:ask "context" [ xw:set-color white ]
  xw:ask xw:widgets xw:with [xw:tab = "context" and xw:kind != "NOTE"] [ xw:set-color blue + 3 ]
  xw:ask xw:notes xw:with [xw:tab = "context"] [ xw:set-color blue - 1
                                                 xw:set-font-color white
                                                 xw:set-opaque? TRUE ]
         
end

;--- Advanced Parameters    
to setup-gui-advpar
  
  xw:create-tab "advpar"
  [ xw:set-order 10
    xw:set-title "Advanced Parameters"
  ]
  
  ; Operational - travel
  
  xw:create-note "advpar-h1"
  [ xw:set-text "Travel for contacts elsewhere"
    xw:set-y 5
  ]
  
  xw:create-slider "travel-rate"
  [ xw:set-label "Travel rate"
    xw:set-y 40
    xw:set-increment 0.05
    xw:set-maximum 1.0
  ]
  
  xw:create-slider "travel-short"
  [ xw:set-label "Travel proportion short"
    xw:set-y 90
    xw:set-increment 0.05
    xw:set-maximum 1.0
  ]
  
  ; Operational - control
  
  xw:create-note "advpar-h2"
  [ xw:set-text "Operational parameters"
    xw:set-y 170
  ]
  
  xw:create-numeric-input "when-declared"
  [ xw:set-label "Prevalence at which epidemic declared"
    xw:set-y 205
  ]

  xw:create-slider "see-distance"
  [ xw:set-label "See distance"
    xw:set-y 265
    xw:set-minimum 1
    xw:set-maximum 5
    xw:set-increment 1
  ]
  
  xw:create-chooser "numPP-persons"
  [ xw:set-label "Population represented by person"
    xw:set-y 325
    xw:set-items (list 1000 2000 5000 10000)
  ]
  
  xw:create-checkbox "randomise?"
  [ xw:set-label "Randomise?"
    xw:set-y 385
  ]
  
  xw:create-numeric-input "random-control"
  [ xw:set-label "Random seed value"
    xw:set-y 410
  ]
  
  ; Operational - attitude
  
  xw:create-note "advpar-h3"
  [ xw:set-text "Attitude structure"
    xw:set-y 490
  ]
  
  xw:create-slider "in-target-attitude"
  [ xw:set-label "Initial attitude bonus for target group"
    xw:set-y 525
    xw:set-increment 0.01
    xw:set-maximum 0.3
  ]
  
  xw:create-slider "attitude-decay"
  [ xw:set-label "Daily return to initial attitude"
    xw:set-y 575
    xw:set-increment 0.1
    xw:set-maximum 10
    xw:set-units "%"
  ]
  
  ; Communication exposure
  
  xw:create-note "advpar-h4"
  [ xw:set-text "Respond to communication"
    xw:set-y 5
  ]

  xw:create-slider "mass-media-prob"
  [ xw:set-label "See mass media"
    xw:set-y 40
    xw:set-increment 0.05
    xw:set-maximum 1
  ]
  
  xw:create-slider "social-media-prob"
  [ xw:set-label "See social media"
    xw:set-y 90
    xw:set-increment 0.05
    xw:set-maximum 1
  ]

  xw:create-slider "health-media-prob"
  [ xw:set-label "Healthcare worker sees health media"
    xw:set-y 140
    xw:set-increment 0.05
    xw:set-maximum 1
  ]
  
  xw:create-slider "goto-hcw-prob"
  [ xw:set-label "Go to doctor during campaign"
    xw:set-y 190
    xw:set-increment 0.05
    xw:set-maximum 1
  ]
  
  ; Effect of communication

  xw:create-note "advpar-h5"
  [ xw:set-text "Effect of communication"
    xw:set-y 270
  ]
  
  xw:create-slider "acceptance-range"
  [ xw:set-label "Lattitude of acceptance"
    xw:set-y 305
    xw:set-increment 0.05
    xw:set-maximum 0.5
  ]
  
  xw:create-slider "repeat-effect"
  [ xw:set-label "Effectiveness of repeat message"
    xw:set-y 355
    xw:set-increment 0.05
    xw:set-maximum 1
  ]

  xw:create-slider "attitude-prop-M"
  [ xw:set-label "Change: mass media"
    xw:set-y 415
    xw:set-increment 0.05
    xw:set-maximum 1
  ]

  xw:create-slider "attitude-prop-S"
  [ xw:set-label "Change: social media"
    xw:set-y 465
    xw:set-increment 0.05
    xw:set-maximum 1
  ]

  xw:create-slider "attitude-prop-P"
  [ xw:set-label "Change: media for healthcare workers"
    xw:set-y 515
    xw:set-increment 0.05
    xw:set-maximum 1
  ]

  xw:create-slider "attitude-prop-H"
  [ xw:set-label "Change: healthcare advisor"
    xw:set-y 565
    xw:set-increment 0.05
    xw:set-maximum 1
  ]

  xw:create-slider "trust-bonus"
  [ xw:set-label "Trust bonus from information"
    xw:set-y 625
    xw:set-increment 0.01
    xw:set-maximum 0.2
  ]
  
  ; Behaviour decisions

  xw:create-note "advpar-h6"
  [ xw:set-text "Inputs to behaviour decisions"
    xw:set-y 5
  ]
  
  xw:create-slider "flag-duration"
  [ xw:set-label "Duration of norms bonus"
    xw:set-y 40
    xw:set-maximum 30
    xw:set-units "days"
  ]
  
  xw:create-slider "normsV-bonus"
  [ xw:set-label "Bonus for vaccination"
    xw:set-y 90
    xw:set-increment 0.05
    xw:set-maximum 0.5
  ]
  
  xw:create-slider "normsNV-bonus"
  [ xw:set-label "Bonus for other protective behaviour"
    xw:set-y 140
    xw:set-increment 0.05
    xw:set-maximum 0.5
  ]

  xw:create-slider "incidence-discount"
  [ xw:set-label "Daily discount for past incidence"
    xw:set-y 200
    xw:set-increment 0.005
    xw:set-maximum 0.2
  ]
  
  xw:create-slider "worry-relative"
  [ xw:set-label "Threat perception multiplier (1 = H1N1)"
    xw:set-y 250
    xw:set-minimum 1
    xw:set-increment 0.5
    xw:set-maximum 5
  ]
  
  xw:create-note "advpar-h7"
  [ xw:set-text "Weights in behaviour decisions"
    xw:set-y 330
  ]
  
  xw:create-slider "attitude-weight-V"
  [ xw:set-label "Vaccination: attitude weight"
    xw:set-y 365
    xw:set-increment 0.05
    xw:set-maximum 1
  ]
  
  xw:create-slider "norms-weight-V"
  [ xw:set-label "Vaccination: norms weight"
    xw:set-y 415
    xw:set-increment 0.05
    xw:set-maximum 1
  ]
  
  xw:create-slider "attitude-weight-NV"
  [ xw:set-label "Nonvaccination: attitude weight"
    xw:set-y 475
    xw:set-increment 0.05
    xw:set-maximum 1
  ]
  
  xw:create-slider "norms-weight-NV"
  [ xw:set-label "Nonvaccination: norms weight"
    xw:set-y 525
    xw:set-increment 0.05
    xw:set-maximum 1
  ]
  
  ; Formatting
  
  xw:ask [ "advpar-h1" "travel-rate" "travel-short"
           "advpar-h2" "when-declared" "see-distance" "numPP-persons" "randomise?" "random-control"
           "advpar-h3" "in-target-attitude" "attitude-decay"
          ]
  [ xw:set-x 10
    xw:set-width 300
  ]
  
  xw:ask [ "advpar-h4" "mass-media-prob" "social-media-prob" "health-media-prob" "goto-hcw-prob"
           "advpar-h5" "acceptance-range" "repeat-effect" "attitude-prop-M" "attitude-prop-S"
           "attitude-prop-P" "attitude-prop-H" "trust-bonus"
          ]
  [ xw:set-x 320
    xw:set-width 300
  ]

  xw:ask [ "advpar-h6" "flag-duration" "normsV-bonus" "normsNV-bonus"
           "incidence-discount" "worry-relative"
           "advpar-h7" "attitude-weight-V" "norms-weight-V" "attitude-weight-NV" "norms-weight-NV"
         ]
  [ xw:set-x 630
    xw:set-width 300
  ]
  
  xw:ask "advpar" [ xw:set-color white ]
  xw:ask xw:widgets xw:with [xw:tab = "advpar" and xw:kind != "NOTE"] [ xw:set-color blue + 3 ]
  xw:ask xw:notes xw:with [xw:tab = "advpar"] [ xw:set-color blue - 1
                                                xw:set-font-color white 
                                                xw:set-opaque? TRUE]
  
end