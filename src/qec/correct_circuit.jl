using MimiqCircuits

# =============================================================================
# tracking metrics
# =============================================================================

mutable struct QECMetrics
	logical_qubits::Int
	data_qubits::Int
	ancilla_qubits::Int
	classical_bits::Int
	qec_rounds::Int
	physical_gates::Int
end

# =============================================================================
# Check that the arguments are valid
# =============================================================================

if length(ARGS) == 0
	# If no argument is provided, print a message
	println("Usage: julia correct_circuit.jl circuit.pb")
	exit()
end

# If the argument exists, get it
filename = ARGS[1]
# Check if the filename ends with ".pb"
if !endswith(filename, ".pb")
	println("The file '$filename' does not end with '.pb'.")
	exit()
end

# Check if the file exists
if !isfile(filename)
	println("The file '$filename' does not exist.")
	exit()
end

new_file = "$(filename[1:end-3])-corrected.pb"

c = loadproto(filename, Circuit)

const SURFACE_CODE_DISTANCE = 3

metrics = QECMetrics(
	numqubits(c),                   # logical qubits
	0,                              # data qubits (filled later)
	0,                              # ancillas
	0,                              # classical bits
	0,                              # QEC rounds
	0,                              # physical gates
)

const DATA_PER_LOGICAL = 9
const ANCILLA_PER_LOGICAL = 8
const CBITS_PER_LOGICAL = 9

metrics.data_qubits     = metrics.logical_qubits * DATA_PER_LOGICAL
metrics.ancilla_qubits  = metrics.logical_qubits * ANCILLA_PER_LOGICAL
metrics.classical_bits  = metrics.logical_qubits * CBITS_PER_LOGICAL


# =============================================================================
# Define logical functions
# =============================================================================

function add_surface_code_d3(c, data_qubits, ancillas, c_bits, metrics::QECMetrics)
	for _ in 1:3
		metrics.qec_rounds += 1

		push!(c, Reset(), ancillas)
		metrics.physical_gates += length(ancillas)

		push!(c, GateH(), ancillas[1:8])
		metrics.physical_gates += 8

		# X stabilizers
		push!(c, GateCX(), ancillas[1], data_qubits[1])
		push!(c, GateCX(), ancillas[1], data_qubits[2])
		push!(c, GateCX(), ancillas[1], data_qubits[4])
		push!(c, GateCX(), ancillas[1], data_qubits[5])
		metrics.physical_gates += 4

		push!(c, GateCX(), ancillas[2], data_qubits[5])
		push!(c, GateCX(), ancillas[2], data_qubits[6])
		push!(c, GateCX(), ancillas[2], data_qubits[8])
		push!(c, GateCX(), ancillas[2], data_qubits[9])
		metrics.physical_gates += 4

		push!(c, GateCX(), ancillas[3], data_qubits[2])
		push!(c, GateCX(), ancillas[3], data_qubits[3])

		push!(c, GateCX(), ancillas[4], data_qubits[7])
		push!(c, GateCX(), ancillas[4], data_qubits[8])
		metrics.physical_gates += 4

		# Z stabilizers
		push!(c, GateCZ(), ancillas[5], data_qubits[2])
		push!(c, GateCZ(), ancillas[5], data_qubits[3])
		push!(c, GateCZ(), ancillas[5], data_qubits[5])
		push!(c, GateCZ(), ancillas[5], data_qubits[6])
		metrics.physical_gates += 4

		push!(c, GateCZ(), ancillas[6], data_qubits[4])
		push!(c, GateCZ(), ancillas[6], data_qubits[5])
		push!(c, GateCZ(), ancillas[6], data_qubits[7])
		push!(c, GateCZ(), ancillas[6], data_qubits[8])
		metrics.physical_gates += 4

		push!(c, GateCZ(), ancillas[7], data_qubits[1])
		push!(c, GateCZ(), ancillas[7], data_qubits[4])
        metrics.physical_gates += 2

		push!(c, GateCZ(), ancillas[8], data_qubits[6])
		push!(c, GateCZ(), ancillas[8], data_qubits[9])
		metrics.physical_gates += 2

		push!(c, GateH(), ancillas[1:8])
		metrics.physical_gates += 8
		push!(c, Measure(), ancillas[1:8], c_bits[1:8])
		metrics.physical_gates += 8

		# Z corrections when X detected
		push!(c, IfStatement(GateZ(), BitString("10000000")), data_qubits[1], c_bits[1:8]...)
		push!(c, IfStatement(GateZ(), BitString("01000000")), data_qubits[9], c_bits[1:8]...)
		push!(c, IfStatement(GateZ(), BitString("11000000")), data_qubits[5], c_bits[1:8]...)

		push!(c, IfStatement(GateZ(), BitString("00100000")), data_qubits[3], c_bits[1:8]...)
		push!(c, IfStatement(GateZ(), BitString("10100000")), data_qubits[2], c_bits[1:8]...)
		push!(c, IfStatement(GateZ(), BitString("01100000")), [data_qubits[3], data_qubits[9]], c_bits[1:8]...)
		push!(c, IfStatement(GateZ(), BitString("11100000")), [data_qubits[3], data_qubits[5]], c_bits[1:8]...)

		push!(c, IfStatement(GateZ(), BitString("00010000")), data_qubits[7], c_bits[1:8]...)
		push!(c, IfStatement(GateZ(), BitString("10010000")), [data_qubits[1], data_qubits[7]], c_bits[1:8]...)
		push!(c, IfStatement(GateZ(), BitString("01010000")), data_qubits[8], c_bits[1:8]...)
		push!(c, IfStatement(GateZ(), BitString("11010000")), [data_qubits[5], data_qubits[7]], c_bits[1:8]...)

		push!(c, IfStatement(GateZ(), BitString("00110000")), [data_qubits[3], data_qubits[7]], c_bits[1:8]...)
		push!(c, IfStatement(GateZ(), BitString("10110000")), [data_qubits[2], data_qubits[7]], c_bits[1:8]...)
		push!(c, IfStatement(GateZ(), BitString("01110000")), [data_qubits[3], data_qubits[8]], c_bits[1:8]...)
		push!(c, IfStatement(GateZ(), BitString("11110000")), [data_qubits[2], data_qubits[8]], c_bits[1:8]...)

        metrics.physical_gates += 15
	end
end

function logical_indexes(i)
	"""
	Return the ranges of data_qubits, ancillas and c_bits depending on which logical qubit we look at.
	>>> logical_indexes(1)
	(1:9, 10:17, 1:9)
	"""
	data_per_logic = 9
	ancillas_per_logic = 8
	c_bits_per_logic = 9

	data_qubits = ((i-1)*(data_per_logic+ancillas_per_logic)+1):((i-1)*(data_per_logic+ancillas_per_logic)+data_per_logic)
	ancillas = ((i-1)*(data_per_logic+ancillas_per_logic)+data_per_logic+1):((i)*(data_per_logic+ancillas_per_logic))
	c_bits = ((i-1)*data_per_logic+1):((i)*data_per_logic)

	return (data_qubits, ancillas, c_bits)
end

function logical_indexes_t(nb_qubits)
	"""
	Return the range of the qubits specialized on the t gate.
	Those qubits are basically the 10 lasts qubits.
	The last qubit is the auxiliary qubit for quantum teleportation.
	Also return classical bits for quantum teleportation
	>>> logical_indexes_t(2)
	35:44, 19:20
	"""

	nb_qubits += 1
	i = nb_qubits

	data_per_logic = 9
	ancillas_per_logic = 8
	c_bits_per_logic = 9

	data = ((i-1)*(data_per_logic+ancillas_per_logic)+1):((i-1)*(data_per_logic+ancillas_per_logic)+data_per_logic+1)
	c_bits = ((i-1)*data_per_logic+1):((i)*data_per_logic)

	return data, c_bits[1:2]
end

function logical_id(c, l_target)
	data_qubits, _, _ = logical_indexes(l_target)
	push!(c, GateID(), data_qubits)
    metrics.physical_gates += length(data_qubits)
end

function logical_x(c, l_target)
	# X on logical qubit with surface code = apply X on all qubits of a column
	data_qubits, _, _ = logical_indexes(l_target)
	push!(c, GateX(), [data_qubits[2], data_qubits[5], data_qubits[8]])
    metrics.physical_gates += 3
end

function logical_z(c, l_target)
	# Z on logical qubit with surface code = apply Z on all qubits of a row
	data_qubits, _, _ = logical_indexes(l_target)
	push!(c, GateZ(), [data_qubits[4], data_qubits[5], data_qubits[6]])
    metrics.physical_gates += 3
end

function logical_t(c, l_target, nb_qubits)
	"""
	Apply a logical T gate.
	For now, the method used is very simple: apply T gate on the middle data qubit.
	It strangly works...

	Tests have been made for H T H (measure ~85% |0>), and H T T T T H (= H Z H) (measure 100% |1>)
	"""
	data_qubits, _, _ = logical_indexes(l_target)

	push!(c, GateT(), data_qubits[5])
    metrics.physical_gates += 1

	# t_qubits, t_bits = logical_indexes_t(nb_qubits)
	# # Prepare t qubits (H + T)
	# push!(c, GateH(), t_qubits[1:9])
	# push!(c, GateT(), t_qubits[1:9])
	# auxilliary = t_qubits[10]

	# # For each data_qubit
	# for (data_qubit, t_qubit) in zip(data_qubits, t_qubits)
	#     # Use teleportation between data_qubit and t_qubit, with auxilliary
	#     # Reset auxilliary
	#     push!(c, Reset(), [t_qubit, auxilliary])

	#     # Do the quantum teleportation circuit but with H+T instead of |0>
	#     push!(c, GateH(), auxilliary)
	#     push!(c, GateCX(), auxilliary, t_qubit)
	#     push!(c, GateCX(), data_qubit, auxilliary)
	#     push!(c, GateH(), data_qubit)

	#     # Measure auxilliary and data qubit
	#     push!(c, Measure(), [auxilliary, data_qubit], t_bits)

	#     push!(c, IfStatement(GateX(), BitString("1")), t_qubit, t_bits[1])
	#     push!(c, IfStatement(GateZ(), BitString("1")), t_qubit, t_bits[2])

	#     # Swap to get result in data_qubit
	#     push!(c, GateSWAP(), data_qubit, t_qubit)
	# end
end

function logical_swap(c, l_target1, l_target2)
	# Swap every data_qubits and ancillas
	data_t1, ancilla_t1, _ = logical_indexes(l_target1)
	data_t2, ancilla_t2, _ = logical_indexes(l_target2)
	for (physical_t1, physical_t2) in zip(data_t1, data_t2)
		push!(c, GateSWAP(), physical_t1, physical_t2)
	end
	for (physical_t1, physical_t2) in zip(ancilla_t1, ancilla_t2)
		push!(c, GateSWAP(), physical_t1, physical_t2)
	end
    metrics.physical_gates += length(data_t1) + length(ancilla_t1)
end

function logical_measure(c, l_target)
	# Measure all qubits of the logical qubit, and set results in the associated classical bits
	data_qubits, _, c_bits = logical_indexes(l_target)
	for (qbit, cbit) in zip(data_qubits, c_bits)
		push!(c, Measure(), qbit, cbit)
	end
    metrics.physical_gates += length(data_qubits)
end

function correct_logical_qubit(c, l_target, metrics::QECMetrics)
	# Apply surface code for the logical qubit (stabilize state |0>)
	data_qubits, ancillas, c_bits = logical_indexes(l_target)
	add_surface_code_d3(c, data_qubits, ancillas, c_bits, metrics)
end

function logical_cx(c, l_control, l_target)
	# Apply a CX between 2 logical qubits (= apply CX on each pair of data_qubits)
	data_control, _, _ = logical_indexes(l_control)
	data_target, _, _ = logical_indexes(l_target)
	for (physical_control, physical_target) in zip(data_control, data_target)
		push!(c, GateCX(), physical_control, physical_target)
	end
    metrics.physical_gates += length(data_control)
end

function logical_h(c, l_target)
	# Apply H on all physical qubits, and rotate by 90°
	data_qubits, _, _ = logical_indexes(l_target)
	for i in data_qubits
		push!(c, GateH(), i)
	end
    metrics.physical_gates += length(data_qubits)
	"""
	987    789    189    389
	654 -> 654 -> 654 -> 654
	321    321    327    127
	"""
	push!(c, GateSWAP(), data_qubits[9], data_qubits[7])
	push!(c, GateSWAP(), data_qubits[7], data_qubits[1])
	push!(c, GateSWAP(), data_qubits[1], data_qubits[3])
    metrics.physical_gates += 3
	"""
	389    349    329    369
	654 -> 658 -> 658 -> 258
	127    127    147    147
	"""
	push!(c, GateSWAP(), data_qubits[8], data_qubits[4])
	push!(c, GateSWAP(), data_qubits[4], data_qubits[2])
	push!(c, GateSWAP(), data_qubits[2], data_qubits[6])
    metrics.physical_gates += 3
end

function is_in_list(obj, l)
	"""
	Return the obj's index in l if it is in the list.
	Return 0 otherwise.
	"""
	for i in 1:length(l)
		if (obj == l[i])
			return i
		end
	end
	return 0
end

# Verify gates
available_gates = [GateID, GateH, GateX, GateZ, GateCX, GateSWAP, GateT, Measure]
gate_to_function = [logical_id, logical_h, logical_x, logical_z, logical_cx, logical_swap, logical_t, logical_measure]


# =============================================================================
# Create the corrected circuit
# =============================================================================

num_qubits = numqubits(c)
corrected = Circuit()

# Apply surface code for each qubit

for i in 1:num_qubits
	correct_logical_qubit(corrected, i, metrics)
end

for i in 1:length(c)
	op = getoperation(c[i])
	index = is_in_list(typeof(op), available_gates)
	if (index == 0)
		println("Found an unsupported gate: '$op'. Exiting.")
		exit()
	end
	# CX and SWAP gates are on several qubits
	if (index == 4 || index == 5)
		(gate_to_function[index])(corrected, getqubit(c[i], 1), getqubit(c[i], 2))
		# T gate require more arguments
	elseif (index == 6)
		(gate_to_function[index])(corrected, getqubit(c[i], 1), num_qubits)
		# Measure also need other arguments
	elseif (index == 7)
		(gate_to_function[index])(corrected, getqubit(c[i], 1), getbit(c[i], 1))
		# Other gates are straight forward
	else
		(gate_to_function[index])(corrected, getqubit(c[i], 1))
	end
end

# display(corrected)


# =============================================================================
# Save the newly created circuit
# =============================================================================

println("Creating file '$new_file'")

println("\n================ QEC METRICS ================")
println("Logical qubits        : ", metrics.logical_qubits)
println("Physical data qubits  : ", metrics.data_qubits)
println("Ancilla qubits        : ", metrics.ancilla_qubits)
println("Classical bits        : ", metrics.classical_bits)
println("QEC rounds executed   : ", metrics.qec_rounds)
println("Physical gates total  : ", metrics.physical_gates)
println("============================================")

saveproto(new_file, corrected)
