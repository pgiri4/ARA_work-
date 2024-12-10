import numpy as np
from tqdm import tqdm
import sys,click
import matplotlib.pyplot as plt
sys.path.append("/path/to/the/directory of ARA_work-/ARA_work-/example_to_read_ARA_wf")

@click.command()
@click.option('-d', '--data', type=str, help='ex) /data/exp/ARA/2014/unblinded/L1/ARA02/1027/run004434/event004434.root')
@click.option('-s', '--station', type=int, help='ex) /data/user')
@click.option('-y', '--year', type=int, help='ex) /home/mkim/')
def get_sim_data_info(data, station, year, plot_wf = True):

    print('Collecting sim data starts!')

    from tools.ara_sim_mini import ara_root_loader

    num_ants = 16

    
    ara_root = ara_root_loader(data, station, year)
    ara_root.get_sub_info(data, get_angle_info = False)
    num_evts = ara_root.num_evts
    wf_time = ara_root.wf_time
    del year 

    if plot_wf:
       fig, axs = plt.subplots(4, 4, figsize=(12, 12))
    for evt in tqdm(range(10,11)):
        for i in range(4):
            for j in range(4):
                ant = i*4+j
                wf_v = ara_root.get_rf_wfs(evt)

                if plot_wf:
                  axs[i,j].plot(wf_time,wf_v[:, ant])
        
      
    plt.savefig("test.png")


if __name__ == '__main__':
   get_sim_data_info()


