# distributed_protocol_completion
Automated synthesis of distributed protocols from scenarios and requirements using counterexample-guided completion

For an overview, see the paper: "Automatic Synthesis of Distributed Protocols", by Alur and Tripakis, e.g., available here: http://www.ccs.neu.edu/~stavros/papers/sigact2017.pdf

The set of experiments described in that paper can be found under: ./examples/abp/  (see the readme.txt file there).

# Automata specification language

inner ::= {
	        states_declaration?
            input_states_declaration?
			output_states_declaration?
			inputs_declaration
			input_enabled_declaration?
			outputs
			initial_state_declaration
			accepting_state_declaration?
			edge_declaration*
	      }

* input_states [state1, state2, ..., stateN]

For every state state1, state2, ..., stateN:
if the automaton specification has an output edge leaving the state the tool will fail.
If there are no transitions leaving the state, in other words it's an "empty" state,
the tool will only consider input transitions leaving that state.
All the states enumerated in an "input_states" declaration will be added in the automaton
even if they are not included in a "states" declaration or in a transition.

* output_states [state1, state2, ..., stateN]

Same as the "input_states" declaration but for outputs.


# Dependencies
* python library networkx, usually `pip install networkx` installs it.
* Either Gurobi solver and python interface to gurobi. You should be able to open a python interpreter and do "import gurobipy" without any errors. More information here http://www.gurobi.com/
* Or Z3
* python module pygraphviz, only necessary for drawing, `pip install pygraphviz`.
* python module ply, `pip install ply`.

# Running synthesizer
The script `driver.py` is the interface to the synthesizer.
Run `./driver.py --help` to get more information.

Example invocations:

```
./driver.py -b VI -v 1     /* tries to use Gurobi */

./driver.py -b ABP1 -s z3minimum -c -a   /* tries to use Z3 */

```

At the end, the script outputs the automata in the folder figures, but the module pygraphviz is necessary.

The benchmarks used are found in the examples folder.
There the automata are constructed programmatically, one benchmark per file.

# Running most recent synthesizer

python tool.py synthesize examples/abp.txt

python tool.py printcandidates examples/abp.txt

python tool.py modelcheck examples/abp.txt

