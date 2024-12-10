import numpy as np
from tqdm import tqdm
import click
import matplotlib.pyplot as plt
import sys
sys.path.append("path/to/the/directory of ARA_work-/example_to_read_ARA_wf")

@click.command()
@click.option('-d', '--data', type=str, help='ex) /data/exp/ARA/2018/unblinded/L1/ARA04/1027/run004434/event004434.root')
@click.option('-p', '--ped', type=str, help='ex) /data/user/pgiri/OMF_filter/ARA04/ped_full/ped_values_full_A2_R4434.dat')

def waveform_collector(data, ped, plot_wf = True, no_tqdm = False):

    print('Reading events starts!')

    from tools.ara_data_load import ara_uproot_loader

    from tools.ara_data_load import ara_root_loader

    # data config
    ara_uproot = ara_uproot_loader(data)
    trig_type = ara_uproot.get_trig_type()
    num_evts = ara_uproot.num_evts
    st = ara_uproot.station_id
    run = ara_uproot.run
    ara_root = ara_root_loader(data, ped, st, ara_uproot.year)
    del ara_uproot
    col =[]
    # loop over the events
    for evt in range(45,50):
        if trig_type[evt] !=0:### trig_type[evt] =1 will be signal like and trig_type[evt] =0 will be noise like
          print('trig',trig_type[evt]) 
          continue
        print(" for event ", evt)
        # get entry and wf
        ara_root.get_entry(evt)
        ara_root.get_useful_evt(ara_root.cal_type.kLatestCalibWithOutTrimFirstBlock)
        
        # loop over the antennas
        if plot_wf:
           fig, axs = plt.subplots(4, 4, figsize=(12, 12))
        for i in range(4):
            for j in range(4):
                ant = i*4+j
                raw_t, raw_v = ara_root.get_rf_ch_wf(ant)
                if ant ==0 :
                   print(np.asarray(raw_v))
                   col.append(np.array(raw_v))
                if plot_wf:
                  axs[i,j].plot(raw_t,raw_v)
            del raw_t, raw_v
                
        ara_root.del_TGraph()
        ara_root.del_usefulEvt()   
        plt.savefig("test_data.png")
        plt.close()
    del ara_root, num_evts
    print('len ',len(col[0]))

if __name__ == "__main__":
   waveform_collector()  




