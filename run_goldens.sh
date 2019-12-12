#!/bin/bash

if [ ! -e "tool.py" ]; then
    echo "Could not find tool.py"
    echo "Run this script from tool's top level folder"
    exit 1
fi

function run_command {
	command=$1
	output_file=$2
    rm $output_file
    echo "Running \"$command > $output_file\""
    $command > $output_file &
}

run_command "python tool.py synthesize -all examples/abp.txt" "test/goldens/abp.txt"

run_command "python tool.py modelcheck -c examples/abp.txt" "test/goldens/abp_modelcheck_print.txt"

run_command "python tool.py modelcheck examples/abp_with_liveness.txt" "test/goldens/abp_with_liveness_modelcheck_no_print.txt"

run_command "python tool.py modelcheck -c examples/abp_with_liveness.txt" "test/goldens/abp_with_liveness_modelcheck_print.txt"

# Strong non blockingness
run_command "python tool.py modelcheck -snb -c test/simple_strong_non_blocking_violation.txt" "test/goldens/simple_strong_non_blocking_violation_modelcheck_snb_c.txt"

run_command "python tool.py modelcheck -snb test/simple_strong_non_blocking_violation.txt" "test/goldens/simple_strong_non_blocking_violation_modelcheck_snb.txt"

run_command "python tool.py modelcheck test/simple_strong_non_blocking_violation.txt" "test/goldens/simple_strong_non_blocking_violation_modelcheck.txt"

run_command "python tool.py modelcheck -snb test/simple_strong_non_blocking_violation_not_included_message.txt" "test/goldens/simple_strong_non_blocking_violation_not_included_message_modelcheck_snb.txt"

run_command "python tool.py modelcheck -snb test/strong_non_blocking_double_definition1.txt" "test/goldens/strong_non_blocking_double_definition1.txt"

run_command "python tool.py synthesize -snb -s z3manualminimal test/abp_snb_output.txt" "test/goldens/abp_snb_output.txt"

# End strong non blockingness
run_command "python tool.py printcandidates test/input_output_declaration_violation.txt" "test/goldens/input_output_declaration_violation_printcandidates.txt"

run_command "python tool.py synthesize test/complete_protocol.txt" "test/goldens/complete_protocol_synthesize.txt"

run_command "python tool.py synthesize test/unsat_protocol.txt" "test/goldens/unsat_protocol_synthesize.txt"

run_command "python tool.py synthesize -pa examples/abp.txt" "test/goldens/abp_synthesize_pa.txt"

# states declaration
run_command "python tool.py printcandidates test/correct_with_states.txt" "test/goldens/correct_with_states.txt"

run_command "python tool.py modelcheck test/missing_state.txt" "test/goldens/missing_state.txt"

run_command "python tool.py synthesize -pa -snb -s z3manualminimal test/abp_blank_state_in_receiver.txt" "test/goldens/abp_blank_state_in_receiver.txt"

# input enabled
run_command "python tool.py modelcheck test/input_enabled_spec_correct.txt" "test/goldens/input_enabled_spec_correct.txt"

run_command "python tool.py modelcheck test/input_enabled_spec_with_output_channel.txt" "test/goldens/input_enabled_spec_with_output_channel.txt"

run_command "python tool.py synthesize -all -s z3manualminimal test/input_enabled_synthesis.txt" "test/goldens/input_enabled_synthesis.txt"

# Different seeds
run_command "python tool.py synthesize -s z3 test/goldens/abp26_2.txt" "test/goldens/abp26_2_no_seed.output"

run_command "python tool.py synthesize -s z3 -seed 0 test/goldens/abp26_2.txt" "test/goldens/abp26_2_seed_0.output"

run_command "python tool.py synthesize -s z3 -seed 1 test/goldens/abp26_2.txt" "test/goldens/abp26_2_seed_1.output"

# dead transitions
run_command "python tool.py printdeadtransitions test/goldens/abp21_sol.txt" "test/goldens/abp21_sol.output"

# input and output states declarations
run_command "python tool.py synthesize -s z3manualminimal -all test/goldens/abp26_output_states_decl_correct.txt" "test/goldens/abp26_output_states_decl_correct.output"

run_command "python tool.py synthesize -s z3manualminimal -all test/goldens/abp26_output_states_decl_correct2.txt" "test/goldens/abp26_output_states_decl_correct2.output"

run_command "python tool.py synthesize -s z3manualminimal -all test/goldens/abp26_output_states_decl_incorrect.txt" "test/goldens/abp26_output_states_decl_incorrect.output"

# ABP27 with input enabledness
run_command "python tool.py synthesize -s z3manualminimal test/goldens/input_enabledness/abp27_removed8.txt" "test/goldens/input_enabledness/abp27_removed8.output"

run_command "python tool.py synthesize -dead -s z3manualminimal test/goldens/input_enabledness/abp27_removed10.txt" "test/goldens/input_enabledness/abp27_removed10.output"

run_command "python tool.py synthesize -s z3manualminimal test/goldens/input_enabledness/abp27_removed12.txt" "test/goldens/input_enabledness/abp27_removed12.output"

echo "waiting for jobs."
for job in `jobs -p`; do
	echo `jobs -p`
    wait $job
done
