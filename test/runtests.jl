using Test

# Load the module from src
include(joinpath(@__DIR__, "..", "src", "InputHandling.jl"))
using .InputHandling

struct MockGateN
    using Test

    using MimiqCircuits
    include("../src/InputHandling.jl")
    using .InputHandling

    @testset "InputHandling (MIMIQ integration)" begin
        # Single-qubit gate
        c1 = MimiqCircuits.Circuit()
        push!(c1, MimiqCircuits.Instruction(MimiqCircuits.GateX(), 1))
        @test InputHandling.check_gate_size(c1) == true

        # Single-qubit gates
        cx = MimiqCircuits.Circuit()
        push!(cx, MimiqCircuits.Instruction(MimiqCircuits.GateX(), 1))
        println("=======================================================================")
        draw(cx)
        @test draw(InputHandling.filter(cx)) === nothing
        println("=======================================================================")

        cz = MimiqCircuits.Circuit()
        push!(cz, MimiqCircuits.Instruction(MimiqCircuits.GateZ(), 1))
        println("=======================================================================")
        draw(cz)
        @test draw(InputHandling.filter(cz)) === nothing
        println("=======================================================================")

        ch = MimiqCircuits.Circuit()
        push!(ch, MimiqCircuits.Instruction(MimiqCircuits.GateH(), 1))
        println("=======================================================================")
        draw(ch)
        @test draw(InputHandling.filter(ch)) === nothing
        println("=======================================================================")

        c_lots = MimiqCircuits.Circuit()
        push!(c_lots, MimiqCircuits.Instruction(MimiqCircuits.GateX(), 1))
        push!(c_lots, MimiqCircuits.Instruction(MimiqCircuits.GateZ(), 1))
        push!(c_lots, MimiqCircuits.Instruction(MimiqCircuits.GateH(), 1))
        push!(c_lots, MimiqCircuits.Instruction(MimiqCircuits.GateX(), 1))
        push!(c_lots, MimiqCircuits.Instruction(MimiqCircuits.GateT(), 1))
        push!(c_lots, MimiqCircuits.Instruction(MimiqCircuits.GateH(), 1))
        push!(c_lots, MimiqCircuits.Instruction(MimiqCircuits.GateZ(), 1))
        push!(c_lots, MimiqCircuits.Instruction(MimiqCircuits.GateX(), 1))
        println("=======================================================================")
        draw(c_lots)
        @test draw(InputHandling.filter(c_lots)) === nothing
        println("=======================================================================")

        cy = MimiqCircuits.Circuit()
        push!(cy, MimiqCircuits.Instruction(MimiqCircuits.GateY(), 1))
        println("=======================================================================")
        draw(cy)
        @test draw(InputHandling.filter(cy)) === nothing
        println("=======================================================================")

        # Two-qubit gate (CX)
        c2 = MimiqCircuits.Circuit()
        push!(c2, MimiqCircuits.Instruction(MimiqCircuits.GateCX(), 1, 2))
        @test InputHandling.check_gate_size(c2) == true

        c_cz = MimiqCircuits.Circuit()
        push!(c_cz, MimiqCircuits.Instruction(MimiqCircuits.GateCZ(), 1, 2))
        draw(c_cz)
        println("=======================================================================")
        @test draw(InputHandling.filter(c_cz)) === nothing
        println("=======================================================================")
        @test InputHandling.check_gate_size(c2) == true

        c_cy = MimiqCircuits.Circuit()
        push!(c_cy, MimiqCircuits.Instruction(MimiqCircuits.GateCY(), 1, 2))
        draw(c_cy)
        println("=======================================================================")
        @test draw(InputHandling.filter(c_cy)) === nothing
        println("=======================================================================")

        # Three-qubit gate should raise InputError
        c3 = MimiqCircuits.Circuit()
        push!(c3, MimiqCircuits.Instruction(MimiqCircuits.GateCCX(), 1, 2, 3))
        @test_throws InputHandling.InputError InputHandling.check_gate_size(c3)

        # Empty circuit is valid
        c4 = MimiqCircuits.Circuit()
        @test InputHandling.check_gate_size(c4) == true

        # Empty circuit is valid
        c_save = MimiqCircuits.Circuit()
        push!(c_save, MimiqCircuits.Instruction(MimiqCircuits.GateCY(), 1, 2))
        @test InputHandling.filter_and_save(c_save) == true

        c = loadproto("input_clean.pb", MimiqCircuits.Circuit)
        draw(c)
    end
end
