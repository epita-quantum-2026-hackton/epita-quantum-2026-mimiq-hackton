module InputHandling

using MimiqCircuits

export InputError, validate_circuit

VALID = [
    GateX(),
    GateZ(),
    GateH(),
    GateT(),
    GateCX(),
    GateSWAP()
]

ALLOWED = [
    GateY(),
    GateCY(),
    GateCZ()
]

struct InputError <: Exception
    msg::String
end
Base.showerror(io::IO, e::InputError) = print(io, e.msg)

# Helpers for checking circuit
function sanitize_parallel(circuit::MimiqCircuits.Circuit)
    """
    Decompose only the gates of class Parallel
    """
    new_c = MimiqCircuits.Circuit()
    for i in eachindex(circuit)
        ins = circuit[i]
        if getoperation(ins) === MimiqCircuitsBase.Parallel
            gate = getoperation(getoperation(ins))
            s = numqubits(ins)
            for i in 1:s:len(getqubits(inst))
                push!(new_c, gate, getqubits(inst)[i:i+s]...)
            end
        else
            push!(new_c, ins)
        end
    end
    return new_c
end

function check_gate_type(circuit::MimiqCircuits.Circuit)
    """
    Check we are using gates allowed by the computer
    Correct some gates into ones allowed by the computer
    Raise an Exception if the gate cannot be used
    """
    new_c = MimiqCircuits.Circuit()
    for i in eachindex(circuit)
        ins = circuit[i]
        if getoperation(ins) in VALID
            push!(new_c, getoperation(ins), getqubits(ins)...)
        else 
            if getoperation(ins) in ALLOWED
                if getoperation(ins) === GateY()
                    changeY(new_c,  getqubits(ins)...)
                end
                if getoperation(ins) === GateCY()
                    changeCY(new_c,  getqubits(ins)...)
                end
                if getoperation(ins) === GateCZ()
                    changeCZ(new_c,  getqubits(ins)...)
                end
            end
        end
    end

    return new_c
end

function changeY(circuit::MimiqCircuits.Circuit, id::Int)
    """
    Decompose a gate Y into authorized gates
    """
    push!(circuit, MimiqCircuits.Instruction(MimiqCircuits.GateX(), id))
    push!(circuit, MimiqCircuits.Instruction(MimiqCircuits.GateZ(), id))
end

function changeCY(circuit::MimiqCircuits.Circuit, id1::Int,  id2::Int)
    """
    Decompose a gate CY into authorized gates
    """
    push!(circuit, MimiqCircuits.Instruction(MimiqCircuits.GateCX(), [id1, id2]...))
    changeCZ(circuit, id1, id2)
end

function changeCZ(circuit::MimiqCircuits.Circuit, id1::Int,  id2::Int)
    """
    Decompose a gate CZ into authorized gates
    """
    push!(circuit, MimiqCircuits.Instruction(MimiqCircuits.GateH(), id2))
    push!(circuit, MimiqCircuits.Instruction(MimiqCircuits.GateCX(), [id1, id2]...))
    push!(circuit, MimiqCircuits.Instruction(MimiqCircuits.GateH(), id2))
end

function check_gate_size(c::MimiqCircuits.Circuit)
    for i in 1:length(c)
        inst = c[i]
        qtargets = getqubits(inst)
        n = length(qtargets)
        if n > 2
            throw(InputError("Unsupported gate at instruction $(i): gate acts on $(n) qubits (max 2)."))
        end
    end
    return true
end

function filter(circuit::MimiqCircuits.Circuit)
    try
        parallel_san_c = sanitize_parallel(circuit)
        check_gate_size(parallel_san_c)
        typed_c = check_gate_type(parallel_san_c)
        return typed_c
    catch
        throw(InputError("Unsupported gate at instruction: gate acts on qubits (max 2)."))
    end
end

function filter_and_save(circuit::MimiqCircuits.Circuit)
    try
        filtered = filter(circuit)
        saveproto("input_clean.pb", filtered)
        return true
    catch
        throw(InputError("Unexpected error while filtering and saving circuit."))
    end
end

end # module
