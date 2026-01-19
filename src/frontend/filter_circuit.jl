# Load the module from src/frontend
include(joinpath(@__DIR__, "input_handling.jl"))
using .InputHandling

if length(ARGS) == 0
	# If no argument is provided, print a message
	println("Usage: julia filter_circuit.jl circuit.pb")
	exit(1)
end

# If the argument exists, get it
filename = ARGS[1]

# Check if the filename ends with ".pb"
if !endswith(filename, ".pb")
	println("The file '$filename' does not end with '.pb'.")
	exit(1)
end

# Check if the file exists
if !isfile(filename)
	println("The file '$filename' does not exist.")
	exit(1)
end

new_file = "$(filename[1:end-3])-filtered.pb"

InputHandling.main(filename, new_file)
