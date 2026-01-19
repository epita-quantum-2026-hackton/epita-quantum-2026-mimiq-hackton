using Test

# Load the module from src
include(joinpath(@__DIR__, "..", "src", "InputHandling.jl"))
using .InputHandling

struct MockGateN
    using Test

    using MimiqCircuits
    include("../src/InputHandling.jl")
    using .InputHandling

    @testset "InputHandling.validate_circuit (MIMIQ integration)" begin
        # Single-qubit gate
        c1 = MimiqCircuits.Circuit()
        push!(c1, MimiqCircuits.Instruction(MimiqCircuits.GateX(), 1))
        @test InputHandling.validate_circuit(c1) == true

        # Two-qubit gate (CX)
        c2 = MimiqCircuits.Circuit()
        push!(c2, MimiqCircuits.Instruction(MimiqCircuits.GateCX(), 1, 2))
        @test InputHandling.validate_circuit(c2) == true

        # Three-qubit gate should raise InputError
        c3 = MimiqCircuits.Circuit()
        push!(c3, MimiqCircuits.Instruction(MimiqCircuits.GateCCX(), 1, 2, 3))
        @test_throws InputHandling.InputError InputHandling.validate_circuit(c3)

        # Empty circuit is valid
        c4 = MimiqCircuits.Circuit()
        @test InputHandling.validate_circuit(c4) == true
    end
end
