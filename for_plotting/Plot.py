from ROOT import THStack, TCanvas, TGaxis, TH1D, TPad, TFile, gPad
from ROOT import kBlack, kBlue, kGreen, kRed
class Plot(TH1D):
 """Plot helper class
 """
 def __init__(self, *args): 
  """ The constructor. Possible arguments:
      1: fileName, histName - loads plot "histName" from file "fileName"
      2: plotList - list of Plot class instances. Merged into one plot
      3: plotList, True - list of Plot class instances. Combined using THStack
  """
  self.hist = None
  self.hist1 = None
  self.drawOpt = ""
  self.xAxisTitle = None
  self.yAxisTitle = None
  self.zAxisTitle = None 

  # Case 1: load the plot from the ROOT file 
  if len(args)==2 and type(args[0])==str and type(args[1])==str:
   fileName = args[0]
   histName = args[1]
   f = TFile.Open(fileName)
   if f:
    self.hist = f.Get(histName)
    self.hist.SetDirectory(0)
    print "Loaded histogram '{}' from file '{}'".format(histName,fileName)
 
  # case 2: list of plots gets added into a single plot
  elif len(args)==1 and type(args[0])==list and len(args[0])>0:
   plotList = args[0]
   self.hist = plotList[0].hist.Clone()
   for plot in plotList[1:]:
    self.hist.Add(plot.hist)
 
  # case 3: use THStack class to combine plots
  elif len(args)==2 and type(args[0])==list and type(args[1])==bool and args[1] and len(args[0])>0:
   plotList = args[0]
   self.hist = THStack()
   for plot in plotList:
    self.hist.Add(plot.hist)
    # copy other plot attributes (drawOpt, axis titles)
    self.drawOpt = plotList[0].drawOpt
    self.hist.SetTitle(plotList[0].hist.GetTitle())
    # for THStack, axis titles can only be set after the plot is drawn :-(
    self.xAxisTitle = plotList[0].hist.GetXaxis().GetTitle()
    self.yAxisTitle = plotList[0].hist.GetYaxis().GetTitle()
    self.zAxisTitle = plotList[0].hist.GetZaxis().GetTitle()

	# case 5: make ratio plot
  elif len(args)==2 and type(args[0])==list and type(args[1])==str and args[1]=='ratio' and len(args[0])>0:
	 PlotList = args[0]
	 self.hist = PlotList[0].hist
	 self.hist1 = PlotList[1].hist

  # case 4: error
  else:
   raise RuntimeError("Cannot process input arguments '{}'".format(args))
 
 def setStyleSolid(self, color):
  """ Helper method to set style: solid histogram
  """
  if self.hist:
   self.hist.SetFillColor(color)
   self.hist.SetFillStyle(1001)
   self.hist.SetMarkerStyle(0)
   self.drawOpt = "hist"

 def setStyleMarker(self, color, marker = 20):
  """ Helper method to set style: marker with errorbars
  """
  if self.hist:
   self.hist.SetMarkerStyle(marker)
   self.hist.SetMarkerSize(1.)
   self.hist.SetMarkerColor(color)
   self.hist.SetLineColor(color)
   self.drawOpt = ""

 def setStyleErrorbar(self, color, fillPattern = 3345):
  """ Helper method to set style: errorbar
  """
  if self.hist:
   self.hist.SetFillColor(color)
   self.hist.SetFillStyle(fillPattern)
   self.hist.SetMarkerStyle(0)
   self.drawOpt = "E2"

 def draw(self, drawOpt = ""):
  self.hist.Draw("{} {}".format(self.drawOpt, drawOpt))
  # set axis titles if this is a THStack 
  if self.xAxisTitle: self.hist.GetXaxis().SetTitle(self.xAxisTitle)
  if self.yAxisTitle: self.hist.GetYaxis().SetTitle(self.yAxisTitle)
  if self.zAxisTitle: self.hist.GetZaxis().SetTitle(self.zAxisTitle)
  # we have to redraw axes
  gPad.RedrawAxis()
	
 def clone(self ):
  h_clone = self.hist.Clone()
  return h_clone

 def normalizeHist(self):
	 self.hist.Scale(1/self.hist.Integral())

 def rebin(self, nBins):
	 self.hist.Rebin(nBins)

 def createRatio(self):
	 h3 = self.hist.Clone()
	 h3.Divide(self.hist1)
	 return h3

# -------------------------------------------------
# new class Plots to handle two histograms
class Plots(Plot):
 def __init__(self, hist1, hist2):
   self.hist1 = hist1
   self.hist2 = hist2

  # make ratio plot
 def createRatio(self):
   h3 = self.hist1.clone("h3")
   h3.SetLineColor(kBlack)
   h3.SetMarkerStyle(21)
   h3.SetTitle("")
   h3.SetMinimum(0.8)
   h3.SetMaximum(1.35)
   # Set up plot for markers and errors
   h3.Sumw2()
   h3.SetStats(0)
   h3.Divide(self.hist2)
   
   # Adjust y-axis settings
   y = h3.GetYaxis()
   y.SetTitle("ratio h1/h2 ")
   y.SetNdivisions(505)
   y.SetTitleSize(20)
   y.SetTitleFont(43)
   y.SetTitleOffset(1.55)
   y.SetLabelFont(43)
   y.SetLabelSize(15)
   
   # Adjust x-axis settings
   x = h3.GetXaxis()
   x.SetTitleSize(20)
   x.SetTitleFont(43)
   x.SetTitleOffset(4.0)
   x.SetLabelFont(43)
   x.SetLabelSize(15)
   
   return h3

# ---------------------------------------------
# some useful functions
def createCanvasPads():
  c = TCanvas("c", "canvas", 800, 800)
  # Upper histogram plot is pad1
  pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
  pad1.SetBottomMargin(0)  # joins upper and lower plot
  pad1.SetGridx()
  pad1.Draw()
  # Lower ratio plot is pad2
  c.cd()  # returns to main canvas before defining pad2
  pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
  pad2.SetTopMargin(0)  # joins upper and lower plot
  pad2.SetBottomMargin(0.2)
  pad2.SetGridy()
  pad2.Draw()
 
  return c, pad1, pad2
