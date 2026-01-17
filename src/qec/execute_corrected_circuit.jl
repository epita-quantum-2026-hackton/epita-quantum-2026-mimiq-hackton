using MimiqCircuits
conn = connect()

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

# =============================================================================
# Declare function
# =============================================================================

function count_bitstrings(n, res)
    """
    Return the dictionary of results from a execution of a distance-3 surface code circuit
    translated into classical binary strings.
    (for each pack of 9 bits, even number of ones = 0, odd number of ones = 1)
    """
    # Initialize an empty dictionary to store the bitstrings and their counts
    bitstring_counts = Dict{String, Int64}()
    
    # Loop over the samples and count the bitstrings
    for (bs, val) in histsamples(res)
        logical_bitstring = ""
        for i in 1:n
            # Count number of 1 in the data_qubits of the ith qubit
            nb_ones = count(x -> x == '1', string(bs[(i-1)*9 + 1 : i*9]))

            if nb_ones & 1 == 0
                logical_bitstring *= "0" # even number of ones => 0
            else
                logical_bitstring *= "1" # odd number of ones => 1
            end
        end

        if !haskey(bitstring_counts, logical_bitstring)
            bitstring_counts[logical_bitstring] = val
        else
            bitstring_counts[logical_bitstring] += val
        end
    end
    
    return bitstring_counts
end

# =============================================================================
# Execute circuit
# =============================================================================

# Get the corrected circuit filename
filename_corrected = "$(filename[1:end-3])-corrected.pb"

# Load both circuits
logical = loadproto(filename, Circuit)
corrected = loadproto(filename_corrected, Circuit)

# Execute logical circuit
println("Sending job execution of '$filename'...")
job_logical = execute(conn, logical, algorithm="mps", nsamples=1000, label="logical")
# Execute physically corrected circuit
println("Sending job execution of '$filename_corrected'...")
job = execute(conn, corrected, algorithm="mps", nsamples=100, label="physical_corrected")

# Get results of logical circuit
println("Wating results of '$filename'...")
res_logical = getresult(conn, job_logical)
# Get results of physically corrected circuit
println("Wating results of '$filename_corrected'...")
res = getresult(conn, job)

# =============================================================================
# Print results
# =============================================================================

println("\nResults:\n")

println("Logical results ($filename):\n", histsamples(res_logical))
println("\nPhysical_corrected ($filename_corrected):\n", count_bitstrings(numqubits(logical), res))
