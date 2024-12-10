import numpy as np
import os
import ROOT
import uproot
import ctypes
from tqdm import tqdm

# custom lib
from tools.ara_constant import ara_const
import os
#link AraRoot
ROOT.gSystem.Load(os.path.join(os.environ.get('ARA_UTIL_INSTALL_DIR'),'..','AraSim','libAra.so'))
ROOT.gSystem.Load(os.path.abspath(os.path.join(os.environ.get('ARA_UTIL_INSTALL_DIR'),"..","AraSim","libAra.so")))
ROOT.gSystem.Load(os.path.abspath(os.path.join(os.environ.get('ARA_UTIL_INSTALL_DIR'),"lib","libAraEvent.so")))
print(os.path.abspath(os.path.join(os.environ.get('ARA_UTIL_INSTALL_DIR'),"..","AraSim","libAra.so")))
ara_const = ara_const()
num_ants = ara_const.USEFUL_CHAN_PER_STATION


class ara_root_loader:

    def __init__(self, data, st, yrs):

        #geom info
        from tools.ara_data_load import ara_geom_loader
        self.st = st
        self.ara_geom = ara_geom_loader(self.st, yrs,verbose = True) # maybe no need this....

        # open a data file
        self.file = ROOT.TFile.Open(data)

        # load in the event free for this file
        self.evtTree = self.file.Get("eventTree")

        # set the tree address to access our raw data type
        self.realEvt = ROOT.UsefulAtriStationEvent()
        self.evtTree.SetBranchAddress("UsefulAtriStationEvent", ROOT.AddressOf(self.realEvt))

        # get the number of entries in this file
        self.num_evts = int(self.evtTree.GetEntries())
        self.entry_num = np.arange(self.num_evts, dtype = int)
        print('total events:', self.num_evts)

    def get_sub_info(self, data, get_angle_info = False, get_temp_info = False, use_ori_angle = False):

        # tired of dealing with PyROOT.....
        file_uproot = uproot.open(data)

        ara_tree = file_uproot['AraTree']
        settings = ara_tree['settings']
        self.time_step = np.asarray(settings['TIMESTEP'], dtype = float) * 1e9
        self.waveform_length = np.asarray(settings['WAVEFORM_LENGTH'], dtype = int)[0]
        self.wf_time = np.arange(self.waveform_length) * self.time_step - self.waveform_length // 2 * self.time_step

    def get_entry(self, evt):

        # get the event
        self.evtTree.GetEntry(evt)

    def get_rf_ch_wf(self, ant):

        self.gr = self.realEvt.getGraphFromRFChan(ant)
        raw_t = np.frombuffer(self.gr.GetX(),dtype=float,count=-1)
        raw_v = np.frombuffer(self.gr.GetY(),dtype=float,count=-1)

        return raw_t, raw_v

    def del_TGraph(self):

        self.gr.Delete()
        del self.gr

    def get_rf_wfs(self, evt):

        wf_v = np.full((self.waveform_length, num_ants), 0, dtype = float)

        self.get_entry(evt)
        for ant in range(num_ants):
            wf_v[:, ant] = self.get_rf_ch_wf(ant)[1]
            self.del_TGraph()

        return wf_v

