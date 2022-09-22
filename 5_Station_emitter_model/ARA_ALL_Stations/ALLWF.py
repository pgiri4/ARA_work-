import logging
import numpy as np
import argparse
import matplotlib.pyplot as plt
import datetime
from NuRadioReco.utilities import units
import NuRadioReco.detector.detector as detector
import NuRadioReco.modules.io.eventReader

from NuRadioReco.framework.parameters import stationParameters as stnp

logging.basicConfig(level=logging.INFO)

# Parse eventfile as argument
parser = argparse.ArgumentParser(description='NuRadioSim file')
parser.add_argument('inputfilename', type=str,
                            help='path to NuRadioMC simulation result')
parser.add_argument('detectordescription', type=str,
                            help='path to detectordescription')
args = parser.parse_args()
det = detector.Detector(json_filename=args.detectordescription)
#det = det.update((datetime.datetime(2018, 1, 1)))
eventReader = NuRadioReco.modules.io.eventReader.eventReader()
eventReader.begin(args.inputfilename)

for event in eventReader.run():
    for station in event.get_stations():
        station_id = station.get_id()
        for channel in station.iter_channels():
            channel_id = channel.get_id()
            #print(channel_id)
            trace = channel.get_trace()
            times = channel.get_times()
            max_index = trace.argmax(axis =0)
            print("Maximum value for station_"+str(station_id)+'_Channel_'+str(channel_id)+ '  ', trace[max_index]/units.mV)
            plt.plot(times[max_index-100: max_index+100]/units.ns, trace[max_index-100: max_index+100]/units.mV)
            plt.savefig('Plot_traces/trace_Station_'+str(station_id)+ '_Channel_'+str(channel_id)+'.png')
            plt.close()
