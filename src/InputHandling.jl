module InputHandling

using MimiqCircuits

export InputError, validate_circuit

struct InputError <: Exception
    msg::String
end
Base.showerror(io::IO, e::InputError) = print(io, e.msg)

function validate_circuit(c::MimiqCircuits.Circuit)
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

end # module
