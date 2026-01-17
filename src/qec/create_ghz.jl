using MimiqCircuits

c = Circuit()
push!(c, GateH(), 1)
push!(c, GateCX(), 1, 2)
push!(c, Measure(), 1, 1)
push!(c, Measure(), 2, 2)

draw(c)

println("Created file ghz.pb")
saveproto("ghz.pb", c)
