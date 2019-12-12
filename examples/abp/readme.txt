
This directory contains many variants of ABP (Alternating Bit Protocol) for
experimentation.

Run the tool as follows (replacing abp1.txt with your file):

  python ../../tool.py synthesize abp1.txt
  python ../../tool.py printcandidates abp1.txt
  python ../../tool.py modelcheck [-snb] abp1.txt
  python ../../tool.py printdeadtransitions abp1.txt

[-snb] checks strong non-blockingness.

To print counterexamples:

  python ../../tool.py modelcheck -c toto.txt

Faster computation option: 

  -s z3manualminimal

Print dead transitions:

python tool.py printdeadtransitions test/goldens/abp21_sol.txt

Evala ena option ston synthesizer "-seed N" By default 0

The file channels.txt is included in abp models and contains a generic 
channel process.

The variants are as follows:

==============================================================================

- abp1.txt: model initially provided by Christos

==============================================================================

- abp2.txt: the same as abp1.txt but with liveness.txt factored out, and
	possibly commented out. In both cases (liveness commented or not)
	reporting 16 deadlocks, and no safety, no liveness violations.

==============================================================================

- abp3.txt: Used "manual" ("complete") versions of ABP Sender and Receiver.
	No deadlocks nor safety nor liveness violations reported, with or 
	without liveness.txt, and with all 4 combinations of the self-loops 
	in manual_sender.txt.
	Also factored out everything.

==============================================================================

- abp4.txt: the same as abp3.txt but liveness1.txt monitor, which checks
	only one of the properties in liveness.txt, namely, that every
	send is followed by a deliver. No violations reported, as expected.

==============================================================================

- abp5.txt: the same as abp4.txt but with incomplete_sender.txt and
	incomplete_receiver.txt. Verification reports 16 deadlocks.
	Synthesis finds 4 solutions, including
	receiver_abp5_solution1.txt and sender_abp5_solution1.txt .

==============================================================================

- abp6.txt: abp5.txt but with receiver_abp5_solution1.txt and
	sender_abp5_solution1.txt : those were found from abp5.txt.
	Verification reports no problems. Are these solutions correct?
	Not really:
	First, the solution does not satisfy non-blockingness. The latter is
	defined in the arxiv version of our HVC 2014 paper, but has not
	been included in the HVC paper. 
	Second, the solution does not satisfy the property "infinitely often
	send". This property states that every (infinite) execution should
	contain an infinite number of "send".

==============================================================================

- abp7.txt: abp6.txt but with modified sender, in order to detect 
	blockingness. The safety monitor blockingness_monitor1.txt
	is included for that purpose. The tool reports safety violations. 
	The following trace is a safety violating trace
	(the state of "client" is omitted since it's always the same)
	Below:
	receiver stands for receiver_abp5_solution1 
	sender stands for sender_abp5_solution1_blockingness.
	monitor stands for blockingness_monitor1


receiver sender monitor backward_channel forward_channel

initial state:

r0	s0	bm0	c0		c0

	send?	send?	

r0	s1	bm1	c0		c0

	p0!	p0?			p0?

r0	s2	bm2	c0		c1

p0'?					p0'!

r1	s2	bm2	c0		c0

deliver!

r2	s2	bm2	c0		c0

a0!			a0?

r3	s2	bm2	c1		c0

	a0'?	a0'?	a0'!

r3	s3	bm3	c1		c0

	a0'?	a0'?	a0'!

r3	s6	error	c1		c0



==============================================================================

- abp8.txt: abp6.txt but with liveness monitors to check the property:
	infinitely often "send". Two versions of a liveness monitor to
	check this property are included:
	infinitely_often_send.txt and infinitely_often_send_input_complete.txt
	The tool reports liveness violations with both versions.
	The following trace is a violating trace obtained with
	infinitely_often_send.txt :

	send, p0, p0', deliver, a0, a0', send, p1, p1', deliver, a1, a1', 
	send, p0, timeout, p0', deliver, 
	( p0, timeout, a0, p0', p0, a0, p0', a0, timeout, p0, p0', timeout)^omega

	However as this liveness monitor is not input-complete, let us
	ignore it for now.

	The following trace is a violating trace obtained with
	infinitely_often_send_input_complete.txt :

	send, p0, p0', deliver, a0, a0', send, p1, p1', deliver, timeout, a1,
	( p1, p1', timeout, p1, timeout, p1' )^omega

	The detailed trace output by the tool is given below:

Cycle:

Trace to reach cycle
client,receiver_abp5_solution1,sender_abp5_solution1,backward_channel,forward_channel,finite_sends
q0,r0,s0,c0,c0,q0
('client', 'q0', 'send!', 'q0')
('sender_abp5_solution1', 's0', 'send?', 's1')
q0,r0,s1,c0,c0,q0
('sender_abp5_solution1', 's1', 'p0!', 's2')
('forward_channel', 'c0', 'p0?', 'c1')
q0,r0,s2,c0,c1,q0
('forward_channel', 'c1', "p0'!", 'c0')
('receiver_abp5_solution1', 'r0', "p0'?", 'r1')
q0,r1,s2,c0,c0,q0
('receiver_abp5_solution1', 'r1', 'deliver!', 'r2')
('client', 'q0', 'deliver?', 'q0')
q0,r2,s2,c0,c0,q0
('receiver_abp5_solution1', 'r2', 'a0!', 'r3')
('backward_channel', 'c0', 'a0?', 'c1')
q0,r3,s2,c1,c0,q0
('backward_channel', 'c1', "a0'!", 'c1')
	this is the first "abnormal" thing that happens in this trace: the
	backward channel stays at state c1 after delivering a0', instead of
	moving back to c0 as would be the normal behavior
('sender_abp5_solution1', 's2', "a0'?", 's3')
q0,r3,s3,c1,c0,q0
('client', 'q0', 'send!', 'q0')
('sender_abp5_solution1', 's3', 'send?', 's4')
q0,r3,s4,c1,c0,q0
('sender_abp5_solution1', 's4', 'p1!', 's5')
('forward_channel', 'c0', 'p1?', 'c2')
q0,r3,s5,c1,c2,q1
('forward_channel', 'c2', "p1'!", 'c0')
('receiver_abp5_solution1', 'r3', "p1'?", 'r4')
q0,r4,s5,c1,c0,q1
('receiver_abp5_solution1', 'r4', 'deliver!', 'r5')
('client', 'q0', 'deliver?', 'q0')
q0,r5,s5,c1,c0,q1
('client', 'q0', 'timeout!', 'q0')
('sender_abp5_solution1', 's5', 'timeout?', 's4')
q0,r5,s4,c1,c0,q1
('receiver_abp5_solution1', 'r5', 'a1!', 'r0')
('backward_channel', 'c1', 'a1?', 'c1')
	normally, at this point the backward channel would receive "a1", move
	from c0 to c2, etc. however, since the backward channel is at state c1
	and not c0, it simply ignores "a1" (self-loops at c1)
q0,r0,s4,c1,c0,q1
Trace to repeat cycle
q0,r0,s4,c1,c0,q1
('forward_channel', 'c0', 'p1?', 'c2')
('sender_abp5_solution1', 's4', 'p1!', 's5')
q0,r0,s5,c1,c2,q1
('receiver_abp5_solution1', 'r0', "p1'?", 'r0')
('forward_channel', 'c2', "p1'!", 'c0')
q0,r0,s5,c1,c0,q1
('sender_abp5_solution1', 's5', 'timeout?', 's4')
('client', 'q0', 'timeout!', 'q0')
q0,r0,s4,c1,c0,q1
('forward_channel', 'c0', 'p1?', 'c2')
('sender_abp5_solution1', 's4', 'p1!', 's5')
q0,r0,s5,c1,c2,q1
('sender_abp5_solution1', 's5', 'timeout?', 's4')
('client', 'q0', 'timeout!', 'q0')
q0,r0,s4,c1,c2,q1
('receiver_abp5_solution1', 'r0', "p1'?", 'r0')
('forward_channel', 'c2', "p1'!", 'c0')
q0,r0,s4,c1,c0,q1

	The sender keeps moving back and forth between s4 and s5 in the cycle.
	But the real problem is blockingness at s5: the backward channel
	would "like" to deliver (a second) "a0'" but the sender refuses to
	receive such a message at state s5 (blockingness). Therefore, there
	is no fairness violation, because "a0'" is never enabled.


==============================================================================

- abp9.txt: abp6.txt with added strong non-blockingness spec:

$ python ../../tool.py modelcheck -snb abp9.txt
Parsing file abp9.txt
# automata read: 5
# of deadlocks: 0
There are strong non-blockingness violations.
There are no safety violations.
There are no liveness violations

	The trace reported by the tool is:

	send, p0, p0', deliver, a0, a0', send, p1, p1', deliver, a1, a1'

	ending in global state (q0,r0,s0,c2,c2). Presumably here the problem
	is that the backward channel can do a1' but sender cannot receive it...


==============================================================================

- abp10.txt: abp5.txt with added strong non-blockingness spec. Synthesis fails
	to terminate after a while (45mins or so) and process is killed.
	Shifting our attention to manually finding a correct solution.


==============================================================================

- abp4nb.txt: the same as abp4.txt but with strong non-blockingness spec
	added for verification purposes. Verification reports SNB problems:

$ python ../../tool.py modelcheck -snb abp4nb.txt
Parsing file abp4nb.txt
# automata read: 7
# of deadlocks: 0
There are strong non-blockingness violations.
There are no safety violations.
There are no liveness violations

	The trace reported by the tool is:

	send, p0, p0', deliver, a0, a0', send, p1, p1', deliver, a1, p1', a1'

	ending in global state (q0,s0,r5,c2,c0). Again the problem seems to be
	that the backward channel can do a1'! at c2, but the sender at s0 has
	no a1'? transition.

	What this means is that the sender that we thought was correct is not
	correct.

==============================================================================

- abp11.txt: starting from abp4nb.txt, trying to find a correct solution,
	meaning a solution which also satisfies SNB.
	This is done by adding the necessary self-loops to the sender, to 
	obtain manual_sender2.txt .
	We also add "timeout" to the list of SNB messages.
	With these modifications, we obtain a correct solution, it seems:

$ python ../../tool.py modelcheck -snb abp11.txt
Parsing file abp11.txt
# automata read: 7
# of deadlocks: 0
There are no strong non-blockingness violations.
There are no safety violations.
There are no liveness violations

	Update: apparently removing some transitions of the sender results
	in a still correct protocol, in particular:

  		// s0 a0'? s0
	and
		// s3 a1'? s3

	which have now been commented out.

==============================================================================

- abp12.txt: trying to synthesize abp11.txt, by removing transitions from
	the receiver (only, for now), and attempting to let the tool add these
	transitions back. Using incomplete_receiver.txt , the tool succeeds:

stavros@eallap18 ~/synthesis/scenarios/tool/examples/abp
$ python ../../tool.py synthesize -s z3manualminimal -snb abp12.txt
Parsing file abp12.txt
# automata read: 7
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r0')
('receiver', 'r3', "p0'?", 'r2')
{'candidate transitions': 24, 'iterations': 2}
...

==============================================================================

- abp13.txt: continuing trying to synthesize abp11.txt, now by removing
	transitions from the sender as well as the receiver.
	Using incomplete_sender2.txt , the tool succeeds:

stavros@eallap18 ~/synthesis/scenarios/tool/examples/abp
$ time python ../../tool.py synthesize -s z3manualminimal -snb abp13.txt
Parsing file abp13.txt
# automata read: 7
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's3', 'timeout?', 's2')
('sender', 's3', "a0'?", 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's5')
('receiver', 'r0', "p1'?", 'r0')
('receiver', 'r3', "p0'?", 'r3')
{'candidate transitions': 60, 'iterations': 11}

real    0m8.488s
user    0m4.081s
sys     0m1.862s



- still with abp13.txt, but using incomplete_sender3.txt , the tool succeeds:

$ time python ../../tool.py synthesize -s z3manualminimal -snb abp13.txt
Parsing file abp13.txt
# automata read: 7
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's3', 'timeout?', 's3')
('sender', 's3', "a0'?", 's2')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's5', 'timeout?', 's4')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r3')
{'candidate transitions': 66, 'iterations': 14}

real    0m27.841s
user    0m26.231s
sys     0m1.641s


- still with abp13.txt, but using incomplete_sender4.txt , the tool succeeds:

stavros@eallap18 ~/synthesis/scenarios/tool/examples/abp
$ python ../../tool.py synthesize -s z3manualminimal -snb abp13.txt
Parsing file abp13.txt
# automata read: 7
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's3', 'timeout?', 's3')
('sender', 's3', "a0'?", 's1')
('sender', 's2', 'timeout?', 's1')
('sender', 's0', "a1'?", 's5')
('sender', 's0', 'timeout?', 's5')
('sender', 's5', 'timeout?', 's4')
('receiver', 'r0', "p1'?", 'r0')
('receiver', 'r3', "p0'?", 'r2')
{'candidate transitions': 72, 'iterations': 22}

the above takes about 10 mins

- still with abp13.txt, but using incomplete_sender5.txt , the tool succeeds:

$ time python ../../tool.py synthesize -s z3manualminimal -snb abp13.txt
Parsing file abp13.txt
# automata read: 7
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's3', "a0'?", 's3')
('sender', 's3', 'timeout?', 's3')
('sender', 's2', 'timeout?', 's1')
('sender', 's0', "a1'?", 's4')
('sender', 's0', 'timeout?', 's4')
('sender', 's5', "a0'?", 's4')
('sender', 's5', 'timeout?', 's4')
('receiver', 'r0', "p1'?", 'r0')
('receiver', 'r3', "p0'?", 'r2')
{'candidate transitions': 78, 'iterations': 23}

real    332m32.996s
user    332m7.686s
sys     0m3.605s

==============================================================================

- abp14.txt: unfortunately things are a bit more complex than initially
	thought, and abp14 does not satisfy infinitely often send, as one
	might expect. In fact, even abp11, the "manual" solution, doesn't
	satisfy this property. We set out to understand why.

$ python ../../tool.py modelcheck -snb abp11.txt
Parsing file abp11.txt
# automata read: 8
# of deadlocks: 0
There are no strong non-blockingness violations.
There are no safety violations.
There are liveness violations

	The tool reports liveness violations, and looking at the
	counterexample traces reported:

	trace1:	send, p0, p0', deliver, a0, a0', cycle: timeout

	trace2: timeout, cycle: timeout

	We see that timeout is problematic, as it can occur at any time.

==============================================================================

- abp15.txt: a more "complete" ABP which separates Sending Client, Receiving
	Client, and Timer, and thus allows to require SNB for "send".
	It satisfies all properties, including infinitely often "send". 

stavros@eallap18 ~/synthesis/scenarios/tool/examples/abp
$ python ../../tool.py modelcheck -snb abp15.txt
Parsing file abp15.txt
# automata read: 10
# of deadlocks: 0
There are no strong non-blockingness violations.
There are no safety violations.
There are no liveness violations

==============================================================================

- abp16.txt: Now that we have found manually "the" correct protocol abp15.txt,
	let's see to what extent we can synthesize it automatically.

	abp16.txt uses "manual_sender3.txt" and "incomplete_receiver.txt"

	The tool succeeds:

stavros@eallap18 ~/synthesis/scenarios/tool/examples/abp
$ python ../../tool.py synthesize -s z3manualminimal -snb abp16.txt
Parsing file abp16.txt
# automata read: 10
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
{'candidate transitions': 44, 'iterations': 5}

==============================================================================

- abp17.txt: uses "incomplete_sender7.txt" and "incomplete_receiver.txt"

	With up to "incomplete 4" (4 hidden transitions) the tool succeeds:

$ time python ../../tool.py synthesize -s z3manualminimal -snb  abp17.txt
Parsing file abp17.txt
# automata read: 10
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'timeout?', 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
{'candidate transitions': 76, 'iterations': 18}

real    0m18.678s
user    0m16.357s
sys     0m2.195s

	With up to "incomplete 5" (5 hidden transitions) the tool suceeds:

$ time python ../../tool.py synthesize -s z3manualminimal -snb  abp17.txt
Parsing file abp17.txt
# automata read: 10
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
{'candidate transitions': 84, 'iterations': 23}

real    4m43.346s
user    4m39.590s
sys     0m2.599s

	For the same, -s z3manualminimal is much faster:

$ time python ../../tool.py synthesize -snb -s z3manualminimal abp17.txt
Parsing file abp17.txt
# automata read: 10
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
{'candidate transitions': 84, 'iterations': 40}

real    0m19.119s
user    0m15.276s
sys     0m3.784s


	With up to "incomplete 8" (all 8 hidden transitions) the tool suceeds:

$ time python ../../tool.py synthesize -snb -s z3manualminimal abp17.txt
Parsing file abp17.txt
# automata read: 10
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's6', "a0'?", 's5')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('receiver', 'r0', "p1'?", 'r5')
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
{'candidate transitions': 108, 'iterations': 52}

real    0m35.286s
user    0m29.369s
sys     0m5.767s



	With -pa option to output the automata:

$ time python ../../tool.py synthesize -snb -s z3manualminimal -pa abp17.txt
Parsing file abp17.txt
# automata read: 10
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's6', "a0'?", 's5')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('receiver', 'r0', "p1'?", 'r5')
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
{'candidate transitions': 108, 'iterations': 52}
When one solution is requested, and one is found, this prints the automata.
Otherwise ignore this.
process sender {
  inputs [send, a0', a1', timeout]
  outputs [p0, done, p1]
  initial s0
  s3 done! s4
  s2 a1'? s1
  s2 a0'? s3
  s2 timeout? s1
  s1 p0! s2
  s0 a1'? s0
  s0 timeout? s0
  s0 send? s1
  s7 done! s0
  s6 a0'? s5
  s6 timeout? s5
  s6 a1'? s7
  s5 p1! s6
  s4 timeout? s4
  s4 send? s5
  s4 a0'? s4
}
process receiver {
  inputs [p0', p1']
  outputs [deliver, a0, a1]
  initial r0
  r4 deliver! r5
  r5 a1! r0
  r0 p0'? r1
  r0 p1'? r5
  r1 deliver! r2
  r2 a0! r3
  r3 p0'? r2
  r3 p1'? r4
}

real    0m35.320s
user    0m29.303s
sys     0m5.940s


	As can be seen from the above output, the synthesized solution for the
	receiver adds exactly the two transitions that were removed, i.e., the
	completed received is identical to manual_receiver.txt .

	As for the sender: the tool adds 8 transitions, as many as were removed.
	Out of these 8 added transitions, 6 are identical to the corresponding
	ones removed. But 2 are slightly different: see completed_sender7.txt
	in particular completed 1 (vs. incomplete 7) and
			completed 4 (vs.  incomplete 3).

==============================================================================

- abp18: built to verify the solutions synthesized from abp17.txt: as
  	expected, the tool reports no violations:

$ time python ../../tool.py modelcheck -snb abp18.txt
Parsing file abp18.txt
# automata read: 10
# of deadlocks: 0
There are no strong non-blockingness violations.
There are no safety violations.
There are no liveness violations

real    0m3.600s
user    0m0.911s
sys     0m1.977s

==============================================================================

- abp19.txt: I realized that abp17.txt had the infinitely often send
  	requirement. What if we try to synthesize a protocol without
	a-priori having this requirement? This is done with abp19.txt .
	The tool still succeeds:

$ time python ../../tool.py synthesize -snb -s z3manualminimal -pa abp19.txt
Parsing file abp19.txt
# automata read: 9
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('receiver', 'r0', "p1'?", 'r5')
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
{'candidate transitions': 108, 'iterations': 50}
When one solution is requested, and one is found, this prints the automata.
Otherwise ignore this.
process sender {
  inputs [send, a0', a1', timeout]
  outputs [p0, done, p1]
  initial s0
  s3 done! s4
  s2 a1'? s1
  s2 a0'? s3
  s2 timeout? s1
  s1 p0! s2
  s0 a1'? s0
  s0 timeout? s0
  s0 send? s1
  s7 done! s0
  s6 a0'? s6
  s6 timeout? s5
  s6 a1'? s7
  s5 p1! s6
  s4 timeout? s4
  s4 send? s5
  s4 a0'? s4
}
process receiver {
  inputs [p0', p1']
  outputs [deliver, a0, a1]
  initial r0
  r4 deliver! r5
  r5 a1! r0
  r0 p0'? r1
  r0 p1'? r5
  r1 deliver! r2
  r2 a0! r3
  r3 p0'? r2
  r3 p1'? r4
}

real    0m40.596s
user    0m34.468s
sys     0m6.023s


Christos notes:

One reasoning that suggests that IOS is implied is the following:
We require that send will be followed by a deliver, after the deliver
we will read the next send due to SNB, which will be followed by deliver
etc etc, hence IOS.
The problem is that SNB does not guarantee that a send will be read after a
deliver has been read.
In fact if you print all solutions for abp19 you get 16 solutions, the same
you got before, but now the receiver can also self loop on the wrong message
in states r0 and r3.
In particular the following is one solution that when modelchecked against IOS
returns a violation.

// Solution
// ** Solution 16 **
// ('sender', 's4', 'timeout?', 's4')
// ('sender', 's4', "a0'?", 's4')
// ('receiver', 'r0', "p1'?", 'r0')
// ('sender', 's2', "a1'?", 's2')
// ('sender', 's2', 'timeout?', 's1')
// ('receiver', 'r3', "p0'?", 'r2')
// ('sender', 's6', 'timeout?', 's5')
// ('sender', 's6', "a0'?", 's6')

==============================================================================

- abp20: built to verify the solutions synthesized from abp19.txt: as
  	expected, the tool reports no violations:

$ time python ../../tool.py modelcheck -snb abp20.txt
Parsing file abp20.txt
# automata read: 10
# of deadlocks: 0
There are no strong non-blockingness violations.
There are no safety violations.
There are no liveness violations

real    0m3.781s
user    0m1.067s
sys     0m1.993s


- addendum: I guess we should also check that every "send" is eventually
  	followed by a "done", since SNB "send" doesn't help if the sender
	never issues a "done". On the other hand, we have verified IOS.
	But we may not include mention of IOS, so ...

	Including liveness3.txt in abp20.txt:

$ python ../../tool.py modelcheck -snb abp20.txt
Parsing file abp20.txt
# automata read: 11
# of deadlocks: 0
There are no strong non-blockingness violations.
There are no safety violations.
There are no liveness violations

==============================================================================

- abp21.txt: What if we try to synthesize while including liveness3.txt ?
	The tool succeeds:

$ time python ../../tool.py synthesize -snb -s z3manualminimal -pa abp21.txt
Parsing file abp21.txt
# automata read: 10
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's6', "a0'?", 's5')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('receiver', 'r0', "p1'?", 'r5')
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
{'candidate transitions': 108, 'iterations': 52}
When one solution is requested, and one is found, this prints the automata.
Otherwise ignore this.
process sender {
  inputs [send, a0', a1', timeout]
  outputs [p0, done, p1]
  initial s0
  s3 done! s4
  s2 a1'? s1
  s2 a0'? s3
  s2 timeout? s1
  s1 p0! s2
  s0 a1'? s0
  s0 timeout? s0
  s0 send? s1
  s7 done! s0
  s6 a0'? s5
  s6 timeout? s5
  s6 a1'? s7
  s5 p1! s6
  s4 timeout? s4
  s4 send? s5
  s4 a0'? s4
}
process receiver {
  inputs [p0', p1']
  outputs [deliver, a0, a1]
  initial r0
  r4 deliver! r5
  r5 a1! r0
  r0 p0'? r1
  r0 p1'? r5
  r1 deliver! r2
  r2 a0! r3
  r3 p0'? r2
  r3 p1'? r4
}

real    0m34.461s
user    0m28.833s
sys     0m5.459s


	Let's also synthesize all solutions from abp21, to make sure ALL of 
	them satisfy IOS, and not just the first one.

$ time python ../../tool.py synthesize -snb -s z3manualminimal -pa -all abp21.txt
Parsing file abp21.txt
# automata read: 10
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's6', "a0'?", 's5')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('receiver', 'r0', "p1'?", 'r5')
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
{'candidate transitions': 108, 'iterations': 52}
SOLUTION #2 FOUND:
** Solution 2 **
('sender', 's6', "a0'?", 's5')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'timeout?', 's1')
('receiver', 'r0', "p1'?", 'r5')
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
{'candidate transitions': 108, 'iterations': 53}
SOLUTION #3 FOUND:
** Solution 3 **
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('receiver', 'r0', "p1'?", 'r5')
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
{'candidate transitions': 108, 'iterations': 92}
SOLUTION #4 FOUND:
** Solution 4 **
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'timeout?', 's1')
('receiver', 'r0', "p1'?", 'r5')
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
{'candidate transitions': 108, 'iterations': 94}
Search finished.
When one solution is requested, and one is found, this prints the automata.
Otherwise ignore this.
process sender {
  inputs [send, a0', a1', timeout]
  outputs [p0, done, p1]
  initial s0
  s3 done! s4
  s2 a0'? s3
  s1 p0! s2
  s0 send? s1
  s7 done! s0
  s6 a1'? s7
  s5 p1! s6
  s4 send? s5
}
process receiver {
  inputs [p0', p1']
  outputs [deliver, a0, a1]
  initial r0
  r4 deliver! r5
  r5 a1! r0
  r0 p0'? r1
  r1 deliver! r2
  r2 a0! r3
  r3 p1'? r4
}

real    0m55.363s
user    0m45.965s
sys     0m8.361s

==============================================================================

- abp22.txt: can we verify by synthesis that no solution exists unless we
	impose fairness assumptions? abp22 attempts to do that.
	The tool reports no solutions:

$ time python ../../tool.py synthesize -snb -s z3manualminimal -pa abp22.txt
Parsing file abp22.txt
# automata read: 10
No solutions could be found.
When one solution is requested, and one is found, this prints the automata.
Otherwise ignore this.
process sender {
  inputs [send, a0', a1', timeout]
  outputs [p0, done, p1]
  initial s0
  s3 done! s4
  s2 a0'? s3
  s1 p0! s2
  s0 send? s1
  s7 done! s0
  s6 a1'? s7
  s5 p1! s6
  s4 send? s5
}
process receiver {
  inputs [p0', p1']
  outputs [deliver, a0, a1]
  initial r0
  r4 deliver! r5
  r5 a1! r0
  r0 p0'? r1
  r1 deliver! r2
  r2 a0! r3
  r3 p1'? r4
}

real    0m34.668s
user    0m28.818s
sys     0m5.863s

	Trying with other fairness constraint removals: you should find
	that channel fairness and receiving client fairness are necessary, 
	while sender fairness is not.


==============================================================================

- abp23.txt: checking that a blocking sender satisfies the safety and two
liveness properties (but not ONB of course):

$ python ../../tool.py modelcheck abp23.txt
Parsing file abp23.txt
# automata read: 10
# of deadlocks: 0
There are no safety violations.
There are no liveness violations

==============================================================================

- abp24.txt: testing the limits of our completion tool: how many
  transitions can we remove until the tool breaks down?

	-- after removing only the last transition from the receiver:

$ time python ../../tool.py synthesize -snb -s z3manualminimal -all abp24.txt
Parsing file abp24.txt
# automata read: 10
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', "a0'?", 's6')
('receiver', 'r5', 'a1!', 'r0')
('receiver', 'r0', "p1'?", 'r5')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
{'candidate transitions': 138, 'iterations': 124}
SOLUTION #2 FOUND:
** Solution 2 **
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('receiver', 'r5', 'a1!', 'r0')
('receiver', 'r0', "p1'?", 'r5')
('sender', 's6', 'timeout?', 's5')
('sender', 's6', "a0'?", 's5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
{'candidate transitions': 138, 'iterations': 125}
SOLUTION #3 FOUND:
** Solution 3 **
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', "a0'?", 's6')
('receiver', 'r5', 'a1!', 'r0')
('receiver', 'r0', "p1'?", 'r5')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
{'candidate transitions': 138, 'iterations': 126}
SOLUTION #4 FOUND:
** Solution 4 **
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('receiver', 'r5', 'a1!', 'r0')
('receiver', 'r0', "p1'?", 'r5')
('sender', 's6', 'timeout?', 's5')
('sender', 's6', "a0'?", 's5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
{'candidate transitions': 138, 'iterations': 127}
Search finished.

real    1m29.782s
user    1m11.239s
sys     0m13.899s


	-- after removing the last two transitions from the receiver:

$ time python ../../tool.py synthesize -snb -s z3manualminimal -all abp24.txt
Parsing file abp24.txt
# automata read: 10
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r4', 'deliver!', 'r5')
('receiver', 'r5', 'a1!', 'r0')
{'candidate transitions': 168, 'iterations': 432}
SOLUTION #2 FOUND:
** Solution 2 **
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r4', 'deliver!', 'r5')
('receiver', 'r5', 'a1!', 'r0')
{'candidate transitions': 168, 'iterations': 434}
SOLUTION #3 FOUND:
** Solution 3 **
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's5')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r4', 'deliver!', 'r5')
('receiver', 'r5', 'a1!', 'r0')
{'candidate transitions': 168, 'iterations': 440}
SOLUTION #4 FOUND:
** Solution 4 **
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's5')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r4', 'deliver!', 'r5')
('receiver', 'r5', 'a1!', 'r0')
{'candidate transitions': 168, 'iterations': 441}
SOLUTION #5 FOUND:
** Solution 5 **
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's5')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r4', 'deliver!', 'r0')
('receiver', 'r5', 'a1!', 'r0')
{'candidate transitions': 168, 'iterations': 893}
SOLUTION #6 FOUND:
** Solution 6 **
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's5')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r4', 'deliver!', 'r0')
('receiver', 'r5', 'a1!', 'r0')
{'candidate transitions': 168, 'iterations': 898}
SOLUTION #7 FOUND:
** Solution 7 **
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r4', 'deliver!', 'r0')
('receiver', 'r5', 'a1!', 'r0')
{'candidate transitions': 168, 'iterations': 1070}
SOLUTION #8 FOUND:
** Solution 8 **
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r4', 'deliver!', 'r0')
('receiver', 'r5', 'a1!', 'r0')
{'candidate transitions': 168, 'iterations': 1071}
Search finished.

real    19m25.611s
user    16m42.609s
sys     2m30.645s



	-- after removing the last three transitions from the receiver:

$ time python ../../tool.py synthesize -snb -s z3manualminimal -all abp24.txt
Parsing file abp24.txt
# automata read: 10
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r4')
('receiver', 'r3', "p1'?", 'r5')
('sender', 's2', "a1'?", 's2')
('receiver', 'r4', 'a1!', 'r0')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r5', 'deliver!', 'r4')
('sender', 's2', 'timeout?', 's1')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 192, 'iterations': 1103}
SOLUTION #2 FOUND:
** Solution 2 **
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r4')
('receiver', 'r3', "p1'?", 'r5')
('receiver', 'r4', 'a1!', 'r0')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r5', 'deliver!', 'r4')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'timeout?', 's1')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 192, 'iterations': 1105}
SOLUTION #3 FOUND:
** Solution 3 **
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p1'?", 'r4')
('receiver', 'r4', 'deliver!', 'r0')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's6', "a0'?", 's5')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'timeout?', 's1')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 192, 'iterations': 2177}
SOLUTION #4 FOUND:
** Solution 4 **
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p1'?", 'r4')
('sender', 's2', "a1'?", 's2')
('receiver', 'r4', 'deliver!', 'r0')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's6', "a0'?", 's5')
('sender', 's2', 'timeout?', 's1')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 192, 'iterations': 2187}
SOLUTION #5 FOUND:
** Solution 5 **
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p1'?", 'r4')
('sender', 's2', "a1'?", 's2')
('receiver', 'r4', 'deliver!', 'r0')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', 'timeout?', 's1')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 192, 'iterations': 2243}
SOLUTION #6 FOUND:
** Solution 6 **
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p1'?", 'r4')
('receiver', 'r4', 'deliver!', 'r0')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'timeout?', 's1')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 192, 'iterations': 2244}
SOLUTION #7 FOUND:
** Solution 7 **
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r4')
('receiver', 'r3', "p1'?", 'r5')
('receiver', 'r4', 'a1!', 'r0')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's6', "a0'?", 's5')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'timeout?', 's1')
('receiver', 'r5', 'deliver!', 'r0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 192, 'iterations': 3205}
SOLUTION #8 FOUND:
** Solution 8 **
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r4')
('receiver', 'r3', "p1'?", 'r5')
('sender', 's2', "a1'?", 's2')
('receiver', 'r4', 'a1!', 'r0')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's6', "a0'?", 's5')
('sender', 's2', 'timeout?', 's1')
('receiver', 'r5', 'deliver!', 'r0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 192, 'iterations': 3206}
SOLUTION #9 FOUND:
** Solution 9 **
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p1'?", 'r4')
('sender', 's2', "a1'?", 's2')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r4', 'deliver!', 'r5')
('sender', 's6', "a0'?", 's5')
('sender', 's2', 'timeout?', 's1')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 192, 'iterations': 3462}
SOLUTION #10 FOUND:
** Solution 10 **
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p1'?", 'r4')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r4', 'deliver!', 'r5')
('sender', 's6', "a0'?", 's5')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'timeout?', 's1')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 192, 'iterations': 3463}
SOLUTION #11 FOUND:
** Solution 11 **
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p1'?", 'r4')
('sender', 's2', "a1'?", 's2')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r4', 'deliver!', 'r5')
('sender', 's2', 'timeout?', 's1')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 192, 'iterations': 3468}
SOLUTION #12 FOUND:
** Solution 12 **
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p1'?", 'r4')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r4', 'deliver!', 'r5')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'timeout?', 's1')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 192, 'iterations': 3949}
SOLUTION #13 FOUND:
** Solution 13 **
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r4')
('receiver', 'r3', "p1'?", 'r5')
('receiver', 'r4', 'a1!', 'r0')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'timeout?', 's1')
('receiver', 'r5', 'deliver!', 'r0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 192, 'iterations': 4210}
SOLUTION #14 FOUND:
** Solution 14 **
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r4')
('receiver', 'r3', "p1'?", 'r5')
('sender', 's2', "a1'?", 's2')
('receiver', 'r4', 'a1!', 'r0')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', 'timeout?', 's1')
('receiver', 'r5', 'deliver!', 'r0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 192, 'iterations': 4212}
SOLUTION #15 FOUND:
** Solution 15 **
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r4')
('receiver', 'r3', "p1'?", 'r5')
('receiver', 'r4', 'a1!', 'r0')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's6', "a0'?", 's5')
('receiver', 'r5', 'deliver!', 'r4')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'timeout?', 's1')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 192, 'iterations': 4752}
SOLUTION #16 FOUND:
** Solution 16 **
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r4')
('receiver', 'r3', "p1'?", 'r5')
('sender', 's2', "a1'?", 's2')
('receiver', 'r4', 'a1!', 'r0')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's6', "a0'?", 's5')
('receiver', 'r5', 'deliver!', 'r4')
('sender', 's2', 'timeout?', 's1')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 192, 'iterations': 4753}
Search finished.

real    88m33.123s
user    76m22.678s
sys     11m54.482s



	-- after removing the last four transitions from the receiver:

$ time python ../../tool.py synthesize -snb -s z3manualminimal -all abp24.txt
Parsing file abp24.txt
# automata read: 10
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r3')
('receiver', 'r2', 'a0!', 'r5')
('receiver', 'r4', 'deliver!', 'r3')
('receiver', 'r5', "p1'?", 'r4')
('receiver', 'r3', 'a1!', 'r0')
('sender', 's4', 'timeout?', 's4')
('receiver', 'r5', "p0'?", 'r2')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 47835}
SOLUTION #2 FOUND:
** Solution 2 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r3')
('receiver', 'r2', 'a0!', 'r5')
('receiver', 'r4', 'deliver!', 'r3')
('receiver', 'r5', "p1'?", 'r4')
('receiver', 'r3', 'a1!', 'r0')
('sender', 's4', 'timeout?', 's4')
('receiver', 'r5', "p0'?", 'r2')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 47838}
SOLUTION #3 FOUND:
** Solution 3 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r3')
('receiver', 'r2', 'a0!', 'r5')
('receiver', 'r4', 'deliver!', 'r3')
('receiver', 'r5', "p1'?", 'r4')
('sender', 's6', "a0'?", 's5')
('receiver', 'r3', 'a1!', 'r0')
('sender', 's4', 'timeout?', 's4')
('receiver', 'r5', "p0'?", 'r2')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 52546}
SOLUTION #4 FOUND:
** Solution 4 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r3')
('receiver', 'r2', 'a0!', 'r5')
('receiver', 'r4', 'deliver!', 'r3')
('receiver', 'r5', "p1'?", 'r4')
('sender', 's6', "a0'?", 's5')
('receiver', 'r3', 'a1!', 'r0')
('sender', 's4', 'timeout?', 's4')
('receiver', 'r5', "p0'?", 'r2')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 52547}
SOLUTION #5 FOUND:
** Solution 5 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r3')
('receiver', 'r2', 'a0!', 'r5')
('receiver', 'r4', 'deliver!', 'r0')
('receiver', 'r5', "p1'?", 'r4')
('receiver', 'r3', 'a1!', 'r0')
('sender', 's4', 'timeout?', 's4')
('receiver', 'r5', "p0'?", 'r2')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 52562}
SOLUTION #6 FOUND:
** Solution 6 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r3')
('receiver', 'r2', 'a0!', 'r5')
('receiver', 'r4', 'deliver!', 'r0')
('receiver', 'r5', "p1'?", 'r4')
('receiver', 'r3', 'a1!', 'r0')
('sender', 's4', 'timeout?', 's4')
('receiver', 'r5', "p0'?", 'r2')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 52563}
SOLUTION #7 FOUND:
** Solution 7 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r3')
('receiver', 'r2', 'a0!', 'r5')
('receiver', 'r4', 'deliver!', 'r0')
('receiver', 'r5', "p1'?", 'r4')
('sender', 's6', "a0'?", 's5')
('receiver', 'r3', 'a1!', 'r0')
('sender', 's4', 'timeout?', 's4')
('receiver', 'r5', "p0'?", 'r2')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 52573}
SOLUTION #8 FOUND:
** Solution 8 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r3')
('receiver', 'r2', 'a0!', 'r5')
('receiver', 'r4', 'deliver!', 'r0')
('receiver', 'r5', "p1'?", 'r4')
('sender', 's6', "a0'?", 's5')
('receiver', 'r3', 'a1!', 'r0')
('sender', 's4', 'timeout?', 's4')
('receiver', 'r5', "p0'?", 'r2')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 54105}
SOLUTION #9 FOUND:
** Solution 9 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r4')
('receiver', 'r2', 'a0!', 'r5')
('receiver', 'r4', 'a1!', 'r0')
('receiver', 'r3', 'deliver!', 'r0')
('sender', 's4', 'timeout?', 's4')
('receiver', 'r5', "p0'?", 'r2')
('receiver', 'r5', "p1'?", 'r3')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 54314}
SOLUTION #10 FOUND:
** Solution 10 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r4')
('receiver', 'r2', 'a0!', 'r5')
('receiver', 'r4', 'a1!', 'r0')
('receiver', 'r3', 'deliver!', 'r0')
('sender', 's4', 'timeout?', 's4')
('receiver', 'r5', "p0'?", 'r2')
('receiver', 'r5', "p1'?", 'r3')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 54318}
SOLUTION #11 FOUND:
** Solution 11 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r4')
('receiver', 'r2', 'a0!', 'r5')
('receiver', 'r4', 'a1!', 'r0')
('receiver', 'r3', 'deliver!', 'r0')
('sender', 's6', "a0'?", 's5')
('sender', 's4', 'timeout?', 's4')
('receiver', 'r5', "p0'?", 'r2')
('receiver', 'r5', "p1'?", 'r3')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 54324}
SOLUTION #12 FOUND:
** Solution 12 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r4')
('receiver', 'r2', 'a0!', 'r5')
('receiver', 'r4', 'a1!', 'r0')
('receiver', 'r3', 'deliver!', 'r0')
('sender', 's6', "a0'?", 's5')
('sender', 's4', 'timeout?', 's4')
('receiver', 'r5', "p0'?", 'r2')
('receiver', 'r5', "p1'?", 'r3')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 54327}
SOLUTION #13 FOUND:
** Solution 13 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r4')
('receiver', 'r2', 'a0!', 'r5')
('receiver', 'r4', 'a1!', 'r0')
('receiver', 'r3', 'deliver!', 'r4')
('sender', 's4', 'timeout?', 's4')
('receiver', 'r5', "p0'?", 'r2')
('receiver', 'r5', "p1'?", 'r3')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 57916}
SOLUTION #14 FOUND:
** Solution 14 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r4')
('receiver', 'r2', 'a0!', 'r5')
('receiver', 'r4', 'a1!', 'r0')
('receiver', 'r3', 'deliver!', 'r4')
('sender', 's4', 'timeout?', 's4')
('receiver', 'r5', "p0'?", 'r2')
('receiver', 'r5', "p1'?", 'r3')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 57917}
SOLUTION #15 FOUND:
** Solution 15 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r4')
('receiver', 'r2', 'a0!', 'r5')
('receiver', 'r4', 'a1!', 'r0')
('receiver', 'r3', 'deliver!', 'r4')
('sender', 's6', "a0'?", 's5')
('sender', 's4', 'timeout?', 's4')
('receiver', 'r5', "p0'?", 'r2')
('receiver', 'r5', "p1'?", 'r3')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 57920}
SOLUTION #16 FOUND:
** Solution 16 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r4')
('receiver', 'r2', 'a0!', 'r5')
('receiver', 'r4', 'a1!', 'r0')
('receiver', 'r3', 'deliver!', 'r4')
('sender', 's6', "a0'?", 's5')
('sender', 's4', 'timeout?', 's4')
('receiver', 'r5', "p0'?", 'r2')
('receiver', 'r5', "p1'?", 'r3')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 57921}
SOLUTION #17 FOUND:
** Solution 17 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r4', 'deliver!', 'r5')
('receiver', 'r3', "p1'?", 'r4')
('receiver', 'r2', 'a0!', 'r3')
('sender', 's6', "a0'?", 's5')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's4', 'timeout?', 's4')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 57957}
SOLUTION #18 FOUND:
** Solution 18 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r4', 'deliver!', 'r5')
('receiver', 'r3', "p1'?", 'r4')
('receiver', 'r2', 'a0!', 'r3')
('sender', 's6', "a0'?", 's5')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's4', 'timeout?', 's4')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 57958}
SOLUTION #19 FOUND:
** Solution 19 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r4', 'deliver!', 'r5')
('receiver', 'r3', "p1'?", 'r4')
('receiver', 'r2', 'a0!', 'r3')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's4', 'timeout?', 's4')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 57963}
SOLUTION #20 FOUND:
** Solution 20 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r4', 'deliver!', 'r0')
('receiver', 'r3', "p1'?", 'r4')
('receiver', 'r2', 'a0!', 'r3')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's4', 'timeout?', 's4')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 57973}
SOLUTION #21 FOUND:
** Solution 21 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r4', 'deliver!', 'r0')
('receiver', 'r3', "p1'?", 'r4')
('receiver', 'r2', 'a0!', 'r3')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's4', 'timeout?', 's4')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 57974}
SOLUTION #22 FOUND:
** Solution 22 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r4', 'deliver!', 'r0')
('receiver', 'r3', "p1'?", 'r4')
('receiver', 'r2', 'a0!', 'r3')
('sender', 's6', "a0'?", 's5')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's4', 'timeout?', 's4')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 57975}
SOLUTION #23 FOUND:
** Solution 23 **
('sender', 's4', "a0'?", 's4')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r4', 'deliver!', 'r0')
('receiver', 'r3', "p1'?", 'r4')
('receiver', 'r2', 'a0!', 'r3')
('sender', 's6', "a0'?", 's5')
('receiver', 'r3', "p0'?", 'r2')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's4', 'timeout?', 's4')
('sender', 's2', 'timeout?', 's1')
('sender', 's2', "a1'?", 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's0', "a1'?", 's0')
{'candidate transitions': 222, 'iterations': 57976}

stopped after more than 12 hours running...

- abp25.txt : checking the correctness of input-enabled sender and receiver

$ python ../../tool.py modelcheck -snb abp25.txt
Parsing file abp25.txt
# automata read: 10
# of deadlocks: 0
There are no strong non-blockingness violations.
There are no safety violations.
There are no liveness violations

==============================================================================

- abp21_with_input_enabledness.txt : modified version of abp21.txt for
	synthesizing input-enabled sender and receiver
	(Christos used abp17.txt to obtain abp_with_input_enabledness.txt)

$ time python ../../tool.py synthesize -s z3manualminimal -all abp21_with_input_enabledness.txt

stopped after 2m14.776s when it had already found 190 solutions.

==============================================================================

- abp26.txt : testing the limits of the tool, with input-enabledness.
	input-enabledness is simpler to implement, and starts with some
	initial constraints already there, so maybe it converges to a solution
	faster? let's check.

	-- after removing only the last transition from the receiver:

with  include "infinitely_often_send_input_complete.txt" :

$ time python ../../tool.py synthesize -s z3manualminimal abp26.txt
Parsing file abp26.txt
# automata read: 11
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's2', 'send?', 's4')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', "a0'?", 's6')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's0', "a0'?", 's4')
('sender', 's6', 'send?', 's1')
('receiver', 'r0', "p1'?", 'r5')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's6')
('sender', 's4', 'timeout?', 's4')
{'candidate transitions': 138, 'iterations': 174}

real    1m34.095s
user    1m15.296s
sys     0m18.760s


without  include "infinitely_often_send_input_complete.txt" :

$ time python ../../tool.py synthesize -s z3manualminimal abp26.txt
Parsing file abp26.txt
# automata read: 10
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's2', 'send?', 's4')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', "a0'?", 's6')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's0', "a0'?", 's4')
('sender', 's6', 'send?', 's1')
('receiver', 'r0', "p1'?", 'r5')
('sender', 's6', 'timeout?', 's5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's6')
('sender', 's4', 'timeout?', 's4')
{'candidate transitions': 138, 'iterations': 174}

real    1m31.414s
user    1m12.619s
sys     0m18.295s



	-- after removing the last two transitions from the receiver:

with  include "infinitely_often_send_input_complete.txt" :

$ time python ../../tool.py synthesize -s z3manualminimal abp26.txt
Parsing file abp26.txt
# automata read: 11
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', "a1'?", 's2')
('sender', 's0', "a1'?", 's0')
('sender', 's0', "a0'?", 's2')
('receiver', 'r4', 'deliver!', 'r0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', 'send?', 's6')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a1'?", 's0')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's6', "a0'?", 's5')
('sender', 's6', 'timeout?', 's5')
('sender', 's6', 'send?', 's4')
('sender', 's4', "a0'?", 's4')
{'candidate transitions': 168, 'iterations': 742}

real    8m44.382s
user    7m13.569s
sys     1m29.410s

without include "infinitely_often_send_input_complete.txt" :

$ time python ../../tool.py synthesize -s z3manualminimal abp26.txt
Parsing file abp26.txt
# automata read: 10
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's2', 'send?', 's2')
('sender', 's0', "a0'?", 's0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'timeout?', 's1')
('receiver', 'r4', 'deliver!', 'r5')
('sender', 's4', 'timeout?', 's4')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's6', "a0'?", 's5')
('sender', 's6', 'timeout?', 's5')
('sender', 's6', 'send?', 's5')
('sender', 's4', "a1'?", 's6')
('sender', 's4', "a0'?", 's4')
{'candidate transitions': 168, 'iterations': 1397}

real    16m10.534s
user    13m24.600s
sys     2m41.676s



	-- after removing the last three transitions from the receiver:

with include "infinitely_often_send_input_complete.txt" :

$ time python ../../tool.py synthesize -s z3manualminimal abp26.txt
Parsing file abp26.txt
# automata read: 11
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p1'?", 'r4')
('sender', 's4', "a1'?", 's7')
('sender', 's2', 'send?', 's0')
('sender', 's2', "a1'?", 's2')
('receiver', 'r4', 'deliver!', 'r0')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's6', "a0'?", 's5')
('sender', 's6', 'send?', 's7')
('sender', 's2', 'timeout?', 's1')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', "a0'?", 's7')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 192, 'iterations': 2368}

real    32m50.593s
user    27m12.844s
sys     5m29.371s


without include "infinitely_often_send_input_complete.txt" :

$ time python ../../tool.py synthesize -s z3manualminimal abp26.txt
Parsing file abp26.txt
# automata read: 10
SOLUTION #1 FOUND:
** Solution 1 **
('sender', 's4', 'timeout?', 's4')
('sender', 's4', "a0'?", 's4')
('receiver', 'r0', "p1'?", 'r5')
('sender', 's2', 'send?', 's4')
('receiver', 'r3', "p1'?", 'r4')
('sender', 's4', "a1'?", 's7')
('receiver', 'r4', 'deliver!', 'r0')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's6', 'send?', 's1')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'timeout?', 's1')
('receiver', 'r5', 'a1!', 'r0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's6', "a0'?", 's6')
('sender', 's0', "a0'?", 's2')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 192, 'iterations': 3711}

real    49m43.074s
user    41m11.459s
sys     8m21.820s


	-- after removing the last four transitions from the receiver:

with include "infinitely_often_send_input_complete.txt" :

didn't terminate after more than 1 day of running...


==============================================================================

- abp21_with_fairness_on_outputs.txt : built at the request of Rajeev to
  verify that by moving the fairness constraint on "deliver" from the 
  Receiving Client to the ABP Receiver, we get the same results. Indeed we do.

python ../../tool.py synthesize -snb -s z3manualminimal -all abp21_with_fairness_on_outputs.txt

and then compare with

python ../../tool.py synthesize -snb -s z3manualminimal -all abp21.txt

Also:

- abp15_with_fairness_on_outputs.txt : built to verify the above:

$ python ../../tool.py modelcheck -snb abp15_with_fairness_on_outputs.txt
Parsing file abp15_with_fairness_on_outputs.txt
# automata read: 11
# of deadlocks: 0
There are no strong non-blockingness violations.
There are no safety violations.
There are no liveness violations

==============================================================================

- abp23_with_fairness_on_outputs.txt: checking that a blocking sender 
	satisfies all properties

$ python ../../tool.py modelcheck -snb abp23_with_fairness_on_outputs.txt
Parsing file abp23_with_fairness_on_outputs.txt
# automata read: 11
# of deadlocks: 0
There are no strong non-blockingness violations.
There are no safety violations.
There are no liveness violations

==============================================================================

- abp27.txt : re-running the synthesis experiments (including testing the 
	limits of the tool), with input-enabledness and output-fairness.

-- with up to // removed 1 from the sender:

$ time python ../../tool.py synthesize -s z3 -all abp27.txt

real    0m7.117s
user    0m3.347s
sys     0m3.936s
 1 solution found

-- with up to // removed 2 from the sender:

real    0m9.051s
user    0m5.032s
sys     0m4.023s
 1 solution found

-- with up to // removed 3 from the sender:

real    0m11.063s
user    0m6.814s
sys     0m4.219s
 1 solution found

-- with up to // removed 4 from the sender:

real    0m15.952s
user    0m10.897s
sys     0m4.919s
 1 solution found

-- with up to // removed 5 from the sender:

real    0m15.776s
user    0m10.792s
sys     0m4.807s
 1 solution found

-- with up to // removed 6 from the sender:

real    0m20.351s
user    0m14.581s
sys     0m5.805s
 1 solution found:
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 60, 'iterations': 66}
Search finished.

Up to this point the transitions found are exactly those removed.

-- with up to // removed 7 from the sender:

real    0m26.636s
user    0m20.448s
sys     0m6.090s
 2 solutions found:
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 68, 'iterations': 66}
SOLUTION #2 FOUND:
** Solution 2 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 68, 'iterations': 68}
Search finished.

-- with up to // removed 8 from the sender:
 4 solutions found:
$ time python ../../tool.py synthesize -s z3 -all abp27.txt
Parsing file abp27.txt
# automata read: 11
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 76, 'iterations': 36}
SOLUTION #2 FOUND:
** Solution 2 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 76, 'iterations': 37}
SOLUTION #3 FOUND:
** Solution 3 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's5')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 76, 'iterations': 68}
SOLUTION #4 FOUND:
** Solution 4 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's5')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 76, 'iterations': 72}
Search finished.

real    0m18.505s
user    0m11.930s
sys     0m4.809s


-- with up to // removed 9 from the sender:

{'candidate transitions': 84, 'iterations': 103}
Search finished.

real    0m20.891s
user    0m15.613s
sys     0m4.939s


 32 solutions found: this is 4*8, where 8 are the possibilities for the
 input-enabled transition 9, which could go anywhere...

-- with up to // removed 10 from the sender:

{'candidate transitions': 92, 'iterations': 320}
Search finished.

real    0m56.201s
user    0m49.014s
sys     0m7.152s

 256 solutions found, as expected: 256 = 32*8

-- with up to // removed 11 from the sender:

{'candidate transitions': 100, 'iterations': 2133}
Search finished.

real    5m46.199s
user    5m17.675s
sys     0m27.413s

 2048 solutions found, as expected: 2048 = 256*8

-- with up to // removed 12 from the sender 

$ time python ../../tool.py synthesize -s z3 -all abp27.txt > bla.txt

...
SOLUTION #16384 FOUND:
** Solution 16384 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's2')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'send?', 's7')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's1')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'send?', 's2')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 108, 'iterations': 16471}
Search finished.

real    45m34.369s
user    42m11.501s
sys     3m2.479s



-- Trying different seeds to find other solutions:

$ time python ../../tool.py synthesize -s z3manualminimal -seed 1 abp27.txt
Parsing file abp27.txt
# automata read: 11
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's6')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'send?', 's1')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's6')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'send?', 's4')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 108, 'iterations': 85}

real    0m47.977s
user    0m37.281s
sys     0m10.266s

-- Performance seems better with -s z3:

$ time python ../../tool.py synthesize -s z3 abp27.txt
Parsing file abp27.txt
# automata read: 11
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'send?', 's1')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's5')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'send?', 's5')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 108, 'iterations': 65}

real    0m16.464s
user    0m11.604s
sys     0m4.668s



Up to now, we have reached the point of the incomplete sender and receiver
derived from the scenarios. Next, we start removing even more transitions
to push the limits. But before that let's do some verification first.

==============================================================================

- abp28.txt: built for verification, but also to check for dead transitions

Verification (this shows the the finally manually designed protocol that
is included in the paper is correct):
$ time python ../../tool.py modelcheck -snb abp28.txt
Parsing file abp28.txt
# automata read: 11
# of deadlocks: 0
There are no strong non-blockingness violations.
There are no safety violations.
There are no liveness violations

real    0m3.060s
user    0m0.784s
sys     0m2.053s


Dead transitions (using completed_sender27.txt in abp28.txt):
$ time python ../../tool.py printdeadtransitions abp28.txt
Parsing file abp28.txt
# automata read: 11
Dead transitions for automaton: safety_monitor2
('sm0', 'done?', 'error')
('error', 'done?', 'error')
('error', 'deliver?', 'error')
('sm1', 'deliver?', 'error')
Dead transitions for automaton: deliver_does_not_follow_send
('ld1', 'send?', 'ld1')
Dead transitions for automaton: safety_monitor
('sm1', 'send?', 'error')
('sm0', 'deliver?', 'error')
('error', 'send?', 'error')
('error', 'deliver?', 'error')
Dead transitions for automaton: sender
('s4', "a1'?", 's5')
('s2', 'send?', 's1')
('s6', 'send?', 's5')
('s0', "a0'?", 's0')
Dead transitions for automaton: receiver
Dead transitions for automaton: ReceivingClient
Dead transitions for automaton: done_does_not_follow_send
('ld1', 'send?', 'ld1')
Dead transitions for automaton: forward_channel
Dead transitions for automaton: Timer
Dead transitions for automaton: backward_channel
Dead transitions for automaton: SendingClient
('sc0', 'done?', 'sc0')

real    0m2.805s
user    0m0.677s
sys     0m2.085s


- abp28.txt also contains various "surprising" versions of ABP Receiver 
and Sender found during synthesis, that we want to check for correctness.


==============================================================================

We push the limits by removing even more transitions, which make the
incomplete automata disconnected. Unfortunately we cannot remove
transitions with strong fairness.

-- with up to // removed 13 from the sender:

$ time python ../../tool.py synthesize -s z3manualminimal abp27.txt
Parsing file abp27.txt
# automata read: 11
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's2')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'send?', 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'send?', 's1')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's1')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's5')
('sender', 's6', 'send?', 's3')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 116, 'iterations': 364}

real    3m20.793s
user    2m45.918s
sys     0m32.987s

$ time python ../../tool.py synthesize -s z3 abp27.txt
Parsing file abp27.txt
# automata read: 11
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's3')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'send?', 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'send?', 's2')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's5')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'send?', 's2')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 116, 'iterations': 168}

real    0m22.220s
user    0m16.733s
sys     0m5.418s


-- with up to // removed 14 from the sender:

$ time python ../../tool.py synthesize -s z3manualminimal abp27.txt
Parsing file abp27.txt
# automata read: 11
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's3')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'send?', 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a0'?", 's3')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'send?', 's3')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's0')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's5')
('sender', 's6', 'send?', 's5')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 124, 'iterations': 1930}

real    17m53.597s
user    14m59.327s
sys     2m48.733s


$ time python ../../tool.py synthesize -s z3 abp27.txt
Parsing file abp27.txt
# automata read: 11
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'send?', 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a0'?", 's3')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'send?', 's4')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's7')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'send?', 's4')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 124, 'iterations': 1981}

real    3m18.842s
user    2m58.560s
sys     0m18.755s

Another interesting solution after Christos' latest tool update:
$ time python ../../tool.py synthesize -s z3 abp27.txt
Parsing file abp27.txt
# automata read: 11
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'send?', 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a0'?", 's3')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'send?', 's4')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's1')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'send?', 's0')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 124, 'iterations': 1116}

real    1m47.918s
user    1m34.849s
sys     0m12.424s



-- with up to // removed 15 from the sender:

$ time python ../../tool.py synthesize -s z3 abp27.txt
Parsing file abp27.txt
# automata read: 11
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'send?', 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a0'?", 's3')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'send?', 's4')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's4')
('sender', 's4', 'send?', 's5')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'send?', 's6')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 132, 'iterations': 329}

real    0m38.444s
user    0m30.918s
sys     0m7.427s


-- with up to // removed 16 from the sender:

$ time python ../../tool.py synthesize -s z3 abp27.txt
Parsing file abp27.txt
# automata read: 11
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'send?', 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a0'?", 's3')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'send?', 's5')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's4')
('sender', 's4', 'send?', 's6')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', "a1'?", 's7')
('sender', 's6', 'send?', 's7')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 140, 'iterations': 7305}

real    12m44.871s
user    11m34.700s
sys     1m6.412s


-- with up to // removed 17 from the sender:

$ time python ../../tool.py synthesize -s z3 abp27.txt
Parsing file abp27.txt
# automata read: 11
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'send?', 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's1', 'p0!', 's2')
('sender', 's2', "a0'?", 's3')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'send?', 's5')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's4')
('sender', 's4', 'send?', 's6')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', "a1'?", 's7')
('sender', 's6', 'send?', 's2')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 164, 'iterations': 6674}

real    11m59.568s
user    10m33.516s
sys     1m4.200s


but with another seed:

$ time python ../../tool.py synthesize -s z3 -seed 19 abp27.txt
Parsing file abp27.txt
# automata read: 11
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'send?', 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's1', 'p0!', 's2')
('sender', 's2', "a0'?", 's3')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'send?', 's2')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's4')
('sender', 's4', 'send?', 's5')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', "a1'?", 's7')
('sender', 's6', 'send?', 's2')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 164, 'iterations': 39326}

real    86m30.683s
user    80m4.126s
sys     5m44.624s




==============================================================================

I got this strange it seems solution by hiding all except the don't care
transitions from the sender:

$ time python ../../tool.py synthesize -s z3 abp27.txt
Parsing file abp27.txt
# automata read: 11
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r0')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'send?', 's6')
('sender', 's0', 'timeout?', 's7')
('sender', 's1', 'p0!', 's1')
('sender', 's2', "a0'?", 's2')
('sender', 's2', "a1'?", 's4')
('sender', 's2', 'timeout?', 's4')
('sender', 's3', 'done!', 's1')
('sender', 's4', "a0'?", 's2')
('sender', 's4', 'send?', 's0')
('sender', 's4', 'timeout?', 's3')
('sender', 's5', 'p0!', 's6')
('sender', 's6', "a0'?", 's2')
('sender', 's6', "a1'?", 's7')
('sender', 's6', 'timeout?', 's5')
('sender', 's7', 'p1!', 's0')
{'candidate transitions': 204, 'iterations': 5443}

real    8m58.036s
user    7m57.922s
sys     0m56.947s


==============================================================================

The above solution is both input-enabled and strongly non-blocking:

$ time python ../../tool.py modelcheck -snb abp27strangeSolution.txt
Parsing file abp27strangeSolution.txt
# automata read: 11
# of deadlocks: 0
There are no strong non-blockingness violations.
There are no safety violations.
There are no liveness violations

Yet clearly it's not what we want: enabled the snb.txt monitor to see the 
trace that leads to blocking (send never can happen after that).

==============================================================================

We tried to see if the above pathological solution abp27strangeSolution.txt
can be avoided by requiring input-enabledness on all output states, and in
particular requiring all such states to have self-loops with all inputs.

This doesn't work, however: adding a self-loop with a0'? in the sender at
state s1 results in liveness violations, where the sender keeps ignoring
the correct acknowledgment a0'. See experiments in directory input-enabled/

Allowing the input transitions at output states to be other than just
self-loops would make synthesis much harder, since now we have to find where
to put such transitions. We didn't try to do this, even manually. So we
abandoned this idea.

==============================================================================

In order to avoid solutions like the abp27strangeSolution.txt, we include
the infinitely_often_send_input_complete.txt monitor and run all experiments
again.

$ time python ../../tool.py synthesize -s z3 -all abp27.txt

-- with up to // removed 1 from the sender:

{'candidate transitions': 20, 'iterations': 12}
Search finished.

real    0m9.180s
user    0m4.005s
sys     0m5.186s

gives 1 solution as expected.

-- with up to // removed 2 from the sender:

{'candidate transitions': 28, 'iterations': 19}
Search finished.

real    0m10.845s
user    0m5.547s
sys     0m5.152s

gives 1 solution as expected.

-- with up to // removed 3 from the sender:

{'candidate transitions': 36, 'iterations': 18}
Search finished.

real    0m11.525s
user    0m6.060s
sys     0m5.283s

gives 1 solution as expected.

-- with up to // removed 4 from the sender:

{'candidate transitions': 44, 'iterations': 25}
Search finished.

real    0m13.741s
user    0m8.119s
sys     0m5.278s

gives 1 solution as expected.

-- with up to // removed 5 from the sender:

{'candidate transitions': 52, 'iterations': 43}
Search finished.

real    0m14.042s
user    0m8.187s
sys     0m5.593s

gives 1 solution as expected.

-- with up to // removed 6 from the sender:

{'candidate transitions': 60, 'iterations': 56}
Search finished.

real    0m16.230s
user    0m10.354s
sys     0m5.935s

gives 1 solution as expected.

-- with up to // removed 7 from the sender:

{'candidate transitions': 68, 'iterations': 46}
Search finished.

real    0m16.343s
user    0m10.524s
sys     0m5.827s

gives 2 solutions as expected.

-- with up to // removed 8 from the sender:

{'candidate transitions': 76, 'iterations': 72}
Search finished.

real    0m19.636s
user    0m13.735s
sys     0m5.655s

gives 4 solutions as expected.

-- with up to // removed 9 from the sender:

{'candidate transitions': 84, 'iterations': 103}

real    0m26.936s
user    0m20.211s
sys     0m6.608s

gives 32 solutions as expected.

-- with up to // removed 10 from the sender:

$ time python ../../tool.py synthesize -s z3 -all abp27.txt > bli.txt

{'candidate transitions': 92, 'iterations': 320}

real    1m25.668s
user    1m15.390s
sys     0m9.663s

gives 256 solutions as expected.

-- with up to // removed 11 from the sender:

$ time python ../../tool.py synthesize -s z3 -all abp27.txt > bli.txt

{'candidate transitions': 100, 'iterations': 2133}

real    9m20.080s
user    8m34.826s
sys     0m38.369s

gives 2048 solutions as expected.

-- with up to // removed 12 from the sender:

$ time python ../../tool.py synthesize -s z3 -all abp27.txt > blu.txt

{'candidate transitions': 108, 'iterations': 16471}

real    88m19.355s
user    83m8.890s
sys     5m1.525s

gives 16384 solutions as expected.

==============================================================================

Just to make sure, we disable the // strong_fairness in
client_sending_input_enabled.txt and try to synthesize:

$ time python ../../tool.py synthesize -s z3 -all abp27.txt
Parsing file abp27.txt
# automata read: 12
No solutions could be found.

real    0m19.392s
user    0m13.377s
sys     0m5.773s

As expected we cannot satisfy the infinitely_often_send_input_complete.txt
requirement without this strong_fairness assumption. So we put it back and
continue.


==============================================================================

Pushing the limits:

-- with up to // removed 13 from the sender:

$ time python ../../tool.py synthesize -s z3 abp27.txt
Parsing file abp27.txt
# automata read: 12
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's3')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'send?', 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a1'?", 's1')
('sender', 's2', 'send?', 's2')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's5')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'send?', 's2')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 116, 'iterations': 168}

real    0m24.847s
user    0m18.481s
sys     0m6.225s


-- with up to // removed 14 from the sender:

$ time python ../../tool.py synthesize -s z3 abp27.txt
Parsing file abp27.txt
# automata read: 12
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's3')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'send?', 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a0'?", 's3')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'send?', 's5')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's3')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'send?', 's1')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 124, 'iterations': 1077}

real    2m4.500s
user    1m50.423s
sys     0m13.280s


-- with up to // removed 15 from the sender:

$ time python ../../tool.py synthesize -s z3 abp27.txt
Parsing file abp27.txt
# automata read: 12
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'send?', 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a0'?", 's3')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'send?', 's2')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's2')
('sender', 's4', 'send?', 's6')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', 'send?', 's2')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 132, 'iterations': 447}

real    0m50.731s
user    0m41.834s
sys     0m8.711s


-- with up to // removed 16 from the sender:

$ time python ../../tool.py synthesize -s z3 abp27.txt
Parsing file abp27.txt
# automata read: 12
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'send?', 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's2', "a0'?", 's3')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'send?', 's2')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's7')
('sender', 's4', 'send?', 's6')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', "a1'?", 's7')
('sender', 's6', 'send?', 's0')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 140, 'iterations': 4991}

real    11m36.331s
user    10m38.053s
sys     0m55.371s


-- with up to // removed 17 from the sender:

$ time python ../../tool.py synthesize -s z3 abp27.txt
Parsing file abp27.txt
# automata read: 12
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'send?', 's1')
('sender', 's0', 'timeout?', 's0')
('sender', 's1', 'p0!', 's2')
('sender', 's2', "a0'?", 's3')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'send?', 's1')
('sender', 's2', 'timeout?', 's1')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's4')
('sender', 's4', 'send?', 's5')
('sender', 's4', 'timeout?', 's4')
('sender', 's6', "a0'?", 's6')
('sender', 's6', "a1'?", 's7')
('sender', 's6', 'send?', 's1')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 164, 'iterations': 5272}

real    12m22.554s
user    11m17.430s
sys     1m2.388s


-- with up to // removed 18 from the sender:

$ time python ../../tool.py synthesize -s z3 abp27.txt
Parsing file abp27.txt
# automata read: 12
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'send?', 's4')
('sender', 's0', 'timeout?', 's0')
('sender', 's1', 'done!', 's2')
('sender', 's2', "a0'?", 's2')
('sender', 's2', "a1'?", 's5')
('sender', 's2', 'send?', 's5')
('sender', 's2', 'timeout?', 's2')
('sender', 's3', 'p0!', 's4')
('sender', 's4', "a0'?", 's1')
('sender', 's4', "a1'?", 's4')
('sender', 's4', 'send?', 's4')
('sender', 's4', 'timeout?', 's3')
('sender', 's6', "a0'?", 's5')
('sender', 's6', "a1'?", 's7')
('sender', 's6', 'send?', 's0')
('sender', 's6', 'timeout?', 's5')
{'candidate transitions': 188, 'iterations': 4056}

real    9m20.838s
user    8m27.584s
sys     0m51.186s

This is a very interesting solution, which however seems correct: see
abp27strangeSolution2.txt.


-- with up to // removed 19 from the sender:

$ time python ../../tool.py synthesize -s z3 abp27.txt
Parsing file abp27.txt
# automata read: 12
SOLUTION #1 FOUND:
** Solution 1 **
('receiver', 'r0', "p1'?", 'r5')
('receiver', 'r3', "p0'?", 'r2')
('sender', 's0', "a0'?", 's0')
('sender', 's0', "a1'?", 's0')
('sender', 's0', 'send?', 's2')
('sender', 's0', 'timeout?', 's0')
('sender', 's1', 'p1!', 's6')
('sender', 's2', "a0'?", 's3')
('sender', 's2', "a1'?", 's2')
('sender', 's2', 'send?', 's0')
('sender', 's2', 'timeout?', 's5')
('sender', 's3', 'done!', 's4')
('sender', 's4', "a0'?", 's4')
('sender', 's4', "a1'?", 's4')
('sender', 's4', 'send?', 's1')
('sender', 's4', 'timeout?', 's4')
('sender', 's5', 'p0!', 's2')
('sender', 's6', "a0'?", 's6')
('sender', 's6', "a1'?", 's7')
('sender', 's6', 'send?', 's1')
('sender', 's6', 'timeout?', 's1')
{'candidate transitions': 212, 'iterations': 9001}

real    21m44.552s
user    19m50.575s
sys     1m48.950s


This is also a very interesting solution, which however seems correct: see
abp27strangeSolution3.txt.

-- with up to // removed 20 from the sender:

stopped after running for 4 hours without having returned a solution.

==============================================================================

-- Still trying to understand abp27strangeSolution4.txt.

   This one has been obtained by 

$ time python ../../tool.py synthesize -s z3 -pa abp27.txt
...
real    0m28.159s
user    0m21.602s
sys     0m6.242s

with the following incomplete sender and receiver:

process sender {
  states [s0, s1, s2, s3, s4, s5, s6, s7]
  input_states [s0, s2, s4, s6]
  output_states [s1, s3, s5, s7]
  inputs [send, a0', a1', timeout]
  input_enabled [send, a0', a1', timeout]
  outputs [done, p0, p1]
  initial s0

  // s0 is an "input state"
  s0 send? s1		// removed 13
  s0 a0'? s0 		// removed 9  don't care transition
  // s0 a1'? s0			// removed 5
  // s0 timeout? s0		// removed 4

  // s1 is an "output state"
  s1 p0! s2 strong_fairness // removed 17 SF redundant for verif but added for synthesis

  // s2 is an "input state"
  // s2 a0'? s3			// removed 14
  // s2 a1'? s2			// removed 7
  // s2 timeout? s1		// removed 3
  s2 send? s2		// removed 10  don't care transition

  // s3 is an "output state":
  s3 done! s4 strong_fairness // removed 18 SF redundant for verif but added for synthesis

  // s4 is an "input state"
  s4 send? s5		// removed 15
  // s4 a0'? s4 		// removed 6
  s4 a1'? s4			// removed 11  don't care transition
  // s4 timeout? s4		// removed 2

  // s5 is an "output state"
  s5 p1! s6 strong_fairness // removed 19 SF redundant for verif but added for synthesis

  // s6 is an "input state"
  s6 a1'? s7			// removed 16
  // s6 a0'? s6			// removed 8
  // s6 timeout? s5		// removed 1
  s6 send? s6		// removed 12  don't care transition

  // s7 is an "output state":
  s7 done! s0 strong_fairness // removed 20 SF redundant for verif but added for synthesis
}

process receiver {
  states [r0, r1, r2, r3, r4, r5]
  input_states [r0, r3]
  output_states [r1, r2, r4, r5]
  inputs [p0', p1']
  input_enabled [p0', p1']
  outputs [deliver, a0, a1]
  initial r0

  // r0 is an "input state"
  r0 p0'? r1
  // r0 p1'? r5		// incomplete 1

  // r1 is an "output state"
  // r1 deliver! r2 strong_fairness

  // r2 is an "output state"
  r2 a0! r3 strong_fairness // SF redundant for verif but added for synthesis

  // r3 is an "input state"
  r3 p1'? r4
  // r3 p0'? r2		// incomplete 2

  // r4 is an "output state"
  r4 deliver! r5 strong_fairness

  // r5 is an "output state"
  r5 a1! r0 strong_fairness // SF redundant for verif but added for synthesis
}

This solution is correct:

$ time python ../../tool.py modelcheck -snb abp27strangeSolution4.txt
Parsing file abp27strangeSolution4.txt
# automata read: 12
# of deadlocks: 0
There are no strong non-blockingness violations.
There are no safety violations.
There are no liveness violations

real    0m3.879s
user    0m1.315s
sys     0m2.534s

This solution has many dead transitions:

$ time python ../../tool.py printdeadtransitions abp27strangeSolution4.txt
Parsing file abp27strangeSolution4.txt
# automata read: 12
Dead transitions for automaton: backward_channel
Dead transitions for automaton: SendingClient
('sc0', 'done?', 'sc0')
Dead transitions for automaton: finite_sends
Dead transitions for automaton: receiver
Dead transitions for automaton: Timer
Dead transitions for automaton: forward_channel
Dead transitions for automaton: done_does_not_follow_send
('ld1', 'send?', 'ld1')
Dead transitions for automaton: safety_monitor
('sm1', 'send?', 'error')
('sm0', 'deliver?', 'error')
('error', 'send?', 'error')
('error', 'deliver?', 'error')
Dead transitions for automaton: ReceivingClient
Dead transitions for automaton: deliver_does_not_follow_send
('ld1', 'send?', 'ld1')
Dead transitions for automaton: safety_monitor2
('sm0', 'done?', 'error')
('error', 'done?', 'error')
('error', 'deliver?', 'error')
('sm1', 'deliver?', 'error')
Dead transitions for automaton: sender
('s2', 'send?', 's2')
('s6', 'send?', 's6')
('s0', "a0'?", 's0')
('s3', 'done!', 's4')
('s4', 'send?', 's5')

real    0m3.764s
user    0m1.066s
sys     0m2.504s


