import ROOT
import os

ROOT.gStyle.SetOptStat(0)

XBINS_MLL = [200, 0, 200]
XBINS_PTLL = [50, 0, 50]
CROSSSECTIONS = {
    "drellyan-mll50" : 300,
    "drellyan-mll50-01j" : 300,
}
COLORS =  {
    "drellyan-mll50"    :    ROOT.kRed-4,
    "drellyan-mll50-01j"   :    ROOT.kGreen-3,
}

def process(sample):

    file_open = ROOT.TFile.Open(f"/tmp/GENTUTORIAL/{sample}.root")
    ROOT.gROOT.cd()
    tree = file_open.Get("Events")
    nevents = tree.GetEntries()

    hist_MLL = ROOT.TH1D(f"{sample}_MLL", f"{sample}_MLL", XBINS_MLL[0], XBINS_MLL[1], XBINS_MLL[2])
    hist_PTLL = ROOT.TH1D(f"{sample}_PTLL", f"{sample}_PTLL", XBINS_PTLL[0], XBINS_PTLL[1], XBINS_PTLL[2])

    hist_MLL.SetLineColor(COLORS[sample])
    hist_PTLL.SetLineColor(COLORS[sample])
    hist_MLL.SetLineWidth(2)
    hist_PTLL.SetLineWidth(2)

    for i in range(nevents):
        tree.GetEntry(i)
        els = []
        for j in range(tree.nGenDressedLepton):
            if tree.GenDressedLepton_pdgId[j] == 11 or tree.GenDressedLepton_pdgId[j] == -11:
                vector = ROOT.TLorentzVector()
                vector.SetPtEtaPhiM(tree.GenDressedLepton_pt[j], tree.GenDressedLepton_eta[j], tree.GenDressedLepton_phi[j], tree.GenDressedLepton_mass[j])
                els.append(vector)
            if len(els) == 2:
                break
        if len(els) < 2:
            continue
        mll = (els[0]+els[1]).M()
        ptll = (els[0]+els[1]).Pt()
        hist_MLL.Fill(mll)
        hist_PTLL.Fill(ptll)

    hist_MLL.SetTitle("")
    hist_PTLL.SetTitle("")
    hist_MLL.Scale(CROSSSECTIONS[sample]/nevents)
    hist_PTLL.Scale(CROSSSECTIONS[sample]/nevents)

    file_open.Close()
    return hist_MLL, hist_PTLL

def main():

    hist_MLLs = {}
    hist_PTLLs = {}
    legend = ROOT.TLegend(0.7, 0.6, 0.8, 0.8)
    for sample in ["drellyan-mll50"]:
        hist_MLL, hist_PTLL = process(sample)
        hist_MLLs[sample] = hist_MLL
        hist_PTLLs[sample] = hist_PTLL
        legend.AddEntry(hist_MLLs[sample], sample, "f")

    canvas_MLL = ROOT.TCanvas("MLL", "MLL", 1600, 900)
    for sample in hist_MLLs:
        hist_MLLs[sample].Draw("samehist")
        hist_MLLs[sample].GetYaxis().SetRangeUser(0.01, 1.e+5)
    legend.Draw("same")
    canvas_MLL.SetLogy()
    ROOT.gPad.RedrawAxis()
    canvas_MLL.SaveAs("MLL.pdf")

    canvas_PTLL = ROOT.TCanvas("PTLL", "PTLL", 1600, 900)
    for sample in hist_MLLs:
        hist_PTLLs[sample].Draw("samehist")
    legend.Draw("same")
    ROOT.gPad.RedrawAxis()
    canvas_PTLL.SaveAs("PTLL.pdf")

if __name__ == "__main__":
    main()
