import hist
import pylhe
import matplotlib.pyplot as plt
import argparse
import os

def print_event(events, i):
    '''A function to print the particle content
       (pdgIds and 4-momenta) of the ith event'''
    print(f"Particle content of the {i}th event:")
    print(f"First input particle pdgId: {parts[i,0].id},"
          f" 4-momenta: {parts[i,0].vector}")
    print(f"Second input particle pdgId: {parts[i,1].id},"
          f" 4-momenta: {parts[i,1].vector}")
    for out_i in range(2, len(parts[i])):
        print(f"Output particle {out_i-1} pdgId: {parts[i,out_i].id},"
              f" 4-momenta: {parts[i,out_i].vector}")


parser = argparse.ArgumentParser()
parser.add_argument("input", help="Path to input lhe file")
parser.add_argument("output",  help="Path to folder for saving histograms")
args = parser.parse_args()

lhe_file = pylhe.read_lhe_with_attributes(args.input)
events = pylhe.to_awkward(lhe_file)
parts = events.particles
top = parts[parts.id == 6][:, 0].vector
antitop = parts[parts.id == -6][:, 0].vector

os.makedirs(args.output, exist_ok=True)

# Print the event content for the first event
print_event(events, 0)

# Also save the content of this event diagramatically 
evts_to_display = pylhe.read_lhe(args.input)
next(evts_to_display).graph.render(filename=os.path.join(args.output, "ttbar_evt"), format="pdf", cleanup=True)

# Plot mass of top quark
m_top_hist = hist.Hist.new.Reg(50, 160, 180).Double()
m_top_hist.fill(top.mass,
                weight=events.eventinfo.weight)
artists = m_top_hist.plot1d()
ax = artists[0].stairs.axes
ax.set_yscale("log")
ax.set_xlabel("Top mass [GeV]")
ax.set_ylabel("Counts")
plt.savefig(os.path.join(args.output, "m_top.pdf"))
plt.clf()

# Plot pt of top quark
pt_top_hist = hist.Hist.new.Reg(40, 0, 400).Double()
pt_top_hist.fill(top.pt,
                 weight=events.eventinfo.weight)
artists = pt_top_hist.plot1d()
ax = artists[0].stairs.axes
ax.set_yscale("log")
ax.set_xlabel("Top $p_{T}$ [GeV]")
ax.set_ylabel("Counts")
plt.savefig(os.path.join(args.output, "pt_top.pdf"))
plt.clf()

# Plot mass of ttbar system
m_ttbar_hist = hist.Hist.new.Reg(60, 350, 950).Double()
m_ttbar_hist.fill((top + antitop).mass,
                  weight=events.eventinfo.weight)
artists = m_ttbar_hist.plot1d()
ax = artists[0].stairs.axes
ax.set_yscale("log")
ax.set_xlabel("$t\\bar{t}$ mass [GeV]")
ax.set_ylabel("Counts")
plt.savefig(os.path.join(args.output, "m_ttbar.pdf"))
plt.clf()

