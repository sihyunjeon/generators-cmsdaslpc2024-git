import ROOT
import os

GENMGPATH = os.getenv("GENMGPATH")
ROOT.gSystem.Load(f"{GENMGPATH}/ExRootAnalysis/libExRootAnalysis.so")
ROOT.gStyle.SetOptStat(0)

XBINS_MLL = [200, 0, 200]
XBINS_PTLL = [50, 0, 50]
CROSSSECTIONS = {
    "drellyan-mll50"   :    1507,
    "onshellz"         :    1420
}
COLORS =  {
    "drellyan-mll50"    :    ROOT.kRed-4,
    "onshellz"          :    ROOT.kGreen-3,
}

def process(mll_):

    file_open = ROOT.TFile.Open(f"{GENMGPATH}/standalone-{mll_}/Events/run_01/unweighted_events.root")
    ROOT.gROOT.cd()
    tree = ROOT.ExRootTreeReader(file_open.Get("LHEF"))
    branch = tree.UseBranch("Particle")
    nevents = tree.GetEntries()

    hist_MLL = ROOT.TH1D(f"{mll_}_MLL", f"{mll_}_MLL", XBINS_MLL[0], XBINS_MLL[1], XBINS_MLL[2])
    hist_PTLL = ROOT.TH1D(f"{mll_}_PTLL", f"{mll_}_PTLL", XBINS_PTLL[0], XBINS_PTLL[1], XBINS_PTLL[2])

    hist_MLL.SetLineColor(COLORS[mll_])
    hist_PTLL.SetLineColor(COLORS[mll_])
    hist_MLL.SetLineWidth(2)
    hist_PTLL.SetLineWidth(2)

    for i in range(nevents):
        tree.ReadEntry(i)
        els = []
        for j in range(len(branch)):
            if branch.At(j).PID == 11 or branch.At(j).PID == -11:
                vector = ROOT.TLorentzVector()
                vector.SetPxPyPzE(branch.At(j).Px, branch.At(j).Py, branch.At(j).Pz, branch.At(j).E)
                els.append(vector)
            if len(els) == 2:
                break
        mll = (els[0]+els[1]).M()
        ptll = (els[0]+els[1]).Pt()
        hist_MLL.Fill(mll)
        hist_PTLL.Fill(ptll)

    hist_MLL.SetTitle("")
    hist_PTLL.SetTitle("")
    hist_MLL.Scale(CROSSSECTIONS[mll_]/nevents)
    hist_PTLL.Scale(CROSSSECTIONS[mll_]/nevents)

    file_open.Close()
    return hist_MLL, hist_PTLL

def main():

    hist_MLLs = {}
    hist_PTLLs = {}
    legend = ROOT.TLegend(0.7, 0.6, 0.8, 0.8)
    for mll in ["mll4", "mll10", "mll50"]:
        hist_MLL, hist_PTLL = process(mll)
        hist_MLLs[mll] = hist_MLL
        hist_PTLLs[mll] = hist_PTLL
        legend.AddEntry(hist_MLLs[mll], mll, "f")

    canvas_MLL = ROOT.TCanvas("MLL", "MLL", 1600, 900)
    for mll in hist_MLLs:
        hist_MLLs[mll].Draw("samehist")
        hist_MLLs[mll].GetYaxis().SetRangeUser(0.01, 1.e+5)
    legend.Draw("same")
    canvas_MLL.SetLogy()
    ROOT.gPad.RedrawAxis()
    canvas_MLL.SaveAs("MLL.pdf")

    canvas_PTLL = ROOT.TCanvas("PTLL", "PTLL", 1600, 900)
    for mll in hist_MLLs:
        hist_PTLLs[mll].Draw("samehist")
    legend.Draw("same")
    ROOT.gPad.RedrawAxis()
    canvas_PTLL.SaveAs("PTLL.pdf")

if __name__ == "__main__":
    main()
