from src.EnvironmentalAgent import *

# Create agent
agent = EnvironmentalAgent("7")

# Add reservation
slot, _ = agent.check_slot((10, 20), "2")
agent.reserve_slot(slot, "2")

slot, _ = agent.check_slot((40, 20), "2")
agent.reserve_slot(slot, "2")

# Check slot
slot, _ = agent.check_slot((10, 20), "1")
agent.reserve_slot(slot, "1")
agent.plot()

slot, _ = agent.check_slot((11, 20), "1")
agent.reserve_slot(slot, "1")
agent.plot()

agent.remove_reservations("1")
agent.reserve_slot(slot, "1")
agent.plot()

print(agent.reservations)

plt.show()