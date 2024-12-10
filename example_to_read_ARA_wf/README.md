
#### ### For real data , please go inside the folder real_data and use following commands ################
### Waveform Reader example
#This example is for beginners in ARA work

#You can use this example and read raw waveforms of ARA data

### How to run this example ###

#An eaxample run will be :

python wf_plotter.py -d /data/exp/ARA/2019/unblinded/L1/ARA04/0407/run007026/event007026.root -p /data/ana/ARA/ARA04/ped_full_from_Martin/ped_full_values_A4_run007026.dat




##### For simulated data, please go inside the folder sim_data and use following commands ################

#You can use this example and read the simulated waveforms

#An eaxample run will be :
# (You can keep the year 2018 for all station)

python plot_sim_wf.py -d /data/ana/ARA/ARA02/sim_signal_full/AraOut.signal_E18_F1_A2_R7.txt.run72.root -s 2 -y 2018




