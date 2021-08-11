from Plot import *
from ROOT import TH1D, TCanvas, TLegend, kRed, kGreen, kBlack

# set ATLAS plot style
# from AtlasStyle import setStyle
# setStyle()
import ROOT as root

root.gROOT.SetStyle('ATLAS')

def plotDifferentMu():
  # draw plots
  histNames = ['ph_pt', 'ph_eta', 'delta_z_pv']
  sampleNames = ['data']
  sampleMCs = ['ttyProd_mca_mcd', 'ttyProd_mce', 'ttyDec', 'Bkg']
  canvases = []
  legends = []

  for histName in histNames:

    isMC = True 

    if isMC == False:
      for sampleName in sampleNames:
        # load individual plots
        plots_mu20 = Plot("histograms.{}.AlgMu20.root".format(sampleName), histName)
        plots_mu30 = Plot("histograms.{}.AlgMu30.root".format(sampleName), histName)
        plots_mu50 = Plot("histograms.{}.AlgMu50.root".format(sampleName), histName)

    if isMC:
      # load individual plots
      plot_mu20 = []
      plot_mu30 = []
      plot_mu50 = []
      for sampleMC in sampleMCs:
        plot_mu20 += [ Plot("histograms.{}.AlgMu20.root".format(sampleMC), histName) ]
        plot_mu30 += [ Plot("histograms.{}.AlgMu30.root".format(sampleMC), histName) ]
        plot_mu50 += [ Plot("histograms.{}.AlgMu50.root".format(sampleMC), histName) ]

      # add plots from different samples
      plots_mu20 = Plot(plot_mu20)
      plots_mu30 = Plot(plot_mu30)
      plots_mu50 = Plot(plot_mu50)

    plots_mu20.normalizeHist()
    plots_mu30.normalizeHist()
    plots_mu50.normalizeHist()

    # set style
    plots_mu20.setStyleMarker(kRed)
    plots_mu30.setStyleMarker(kGreen)
    plots_mu50.setStyleMarker(kBlack)

    # create a canvas
    c, pad1, pad2 = createCanvasPads()

    # draw everything
    pad1.cd()
    #plots_mu20.GetXaxis().SetTitle("Normalized to unity")
    plots_mu20.draw()
    plots_mu30.draw("same")
    plots_mu50.draw("same")
    plots2030 = Plot([plots_mu20, plots_mu30], "ratio")
    plots2050 = Plot([plots_mu20, plots_mu50], "ratio")
    plots3050 = Plot([plots_mu30, plots_mu50], "ratio")
    ratio2030= plots2030.createRatio()
    ratio2050= plots2050.createRatio()
    ratio3050 = plots3050.createRatio()
    ratio2050.SetMarkerColor(kRed)
    ratio2050.SetLineColor(kRed)
    ratio3050.SetMarkerColor(kGreen)
    ratio3050.SetLineColor(kGreen)
    pad2.cd()
    ratio2050.GetYaxis().SetRangeUser(0.8, 1.2)
    ratio2050.GetYaxis().SetTitle("#frac{#mu_{x}}{#mu_{50}}")
    ratio2050.GetYaxis().SetTitleSize(.10)
    ratio2050.GetXaxis().SetTitleSize(.10)
    #ratio2030.Draw("ep")
    ratio2050.Draw("ep ")
    ratio3050.Draw("ep same")

    pad1.cd()
    # draw legend
    legend = TLegend(0.6, 0.9, 0.9, 0.65)
    legend.AddEntry(plots_mu20.hist, "mu 20 ", "f")
    legend.AddEntry(plots_mu30.hist, "mu 30 ", "f")
    legend.AddEntry(plots_mu50.hist, "mu 50 ", "f")
    legend.Draw("same")

    pad2.cd()
    # draw legend
    legend1 = TLegend(0.6, 0.9, 0.9, 0.65)
    #legend1.AddEntry(ratio2030, "mu 20/mu 30 ", "f")
    legend1.AddEntry(ratio2050, "mu 20/mu 50 ", "f")
    legend1.AddEntry(ratio3050, "mu 30/mu 50 ", "f")
    legend1.Draw("same")

    # save the canvas
    c.Print("{0}.{1}.svg".format(histName, isMC))

    # save the instances so they are not deleted by the garbage collector
    canvases += [c]
    legends += [ legend ]

def plotDataMC():
  # draw plots
  histNames = ['ph_pt', 'ph_eta', 'delta_z_pv', 'z_ph', 'z_pv']
  sampleNames = ['data']
  sampleMCs = ['ttyProd_mca_mcd', 'ttyProd_mce', 'ttyDec', 'Bkg']
  canvases = []
  legends = []
  #mus = ['Mu20', 'Mu30', 'Mu50', 'Default']
  mus = ['Default']


  for mu in mus:
    for histName in histNames:
      for sampleName in sampleNames:
        # load individual plots
        plot_data = Plot("histograms.{0}.Alg{1}.root".format(sampleName, mu), histName)

      # load individual plots
      plots_mc = []
      for sampleMC in sampleMCs:
        plots_mc += [ Plot("histograms.{0}.Alg{1}.root".format(sampleMC, mu), histName) ]

      # add plots from different samples
      plot_mc = Plot(plots_mc)

      plot_data.normalizeHist()
      plot_mc.normalizeHist()

      # set style
      plot_data.setStyleMarker(kRed)
      plot_mc.setStyleMarker(kGreen)

      # create a canvas
      c, pad1, pad2 = createCanvasPads()

      # draw everything
      pad1.cd()
      #plots_data.GetXaxis().SetTitle("Normalized to unity")
      plot_data.draw()
      plot_mc.draw("same")
      plot_data_mc = Plot([plot_data, plot_mc], "ratio")
      ratio_data_mc = plot_data_mc.createRatio()
      pad2.cd()
      ratio_data_mc.GetYaxis().SetRangeUser(0.6, 1.4)
      ratio_data_mc.GetYaxis().SetTitle("Data/MC")
      ratio_data_mc.GetYaxis().SetTitleSize(.10)
      ratio_data_mc.GetXaxis().SetTitleSize(.10)
      ratio_data_mc.Draw("ep")

      pad1.cd()
      # draw legend
      legend = TLegend(0.6, 0.9, 0.9, 0.65)
      legend.AddEntry(plot_data.hist, "data ", "f")
      legend.AddEntry(plot_mc.hist, "mc  ", "f")
      legend.Draw("same")

      # save the canvas
      c.Print("{0}.{1}.svg".format(histName, mu))

      # save the instances so they are not deleted by the garbage collector
      canvases += [c]
      legends += [ legend ]

# main function
def main():
  #plotDifferentMu()
  plotDataMC()

if __name__ == "__main__":
  main()
