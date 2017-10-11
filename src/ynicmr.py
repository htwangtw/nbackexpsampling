# -*- coding: utf-8 -*-
'''
Usful functions for collecting trigger at YNiC
and using serial port to collect participant responses
'''
# YNiC fMRI trigger related information
import sys
import serial

if sys.platform == 'linux2':
    # in house script ynicstim location
    YNICSTIM = '/groups/stimpc/ynicstim'
    SERIAL_PORT = '/dev/ttyS0'
else:
    YNICSTIM = 'M:/stimpc/ynicstim'
    SERIAL_PORT = 'COM1'
TRIG_PORT = '/dev/parport0'

SLICESPERVOL = 60 # check this information with Charlotte
DUMMY_VOL = 3
sys.path.append(YNICSTIM)

from ynicstim import parallel_compat, trigger
# from src.fileIO import read_only

def get_trig_collector():
    p = parallel_compat.getParallelPort(TRIG_PORT)
    ts = trigger.ParallelInterruptTriggerSource(port=p)
    trig_collector = trigger.TriggerCollector(triggersource=ts,
                                              slicespervol=SLICESPERVOL)
    return trig_collector

def save_vol_time(trig_collector, timer, path):
    trig_collector.endCollection()
    vol_time = trig_collector.getVolumeTimings(timer)
    with open(path, 'w+') as f:
        f.write('Volume,Time\n')
        for i, t in enumerate(vol_time):
            f.write('{:d},{:.3f}\n'.format(i, t))
#            read_only(path)

resp_device = serial.Serial(SERIAL_PORT, 9600, timeout=0.001)

def get_serial(timer, resp_device):
    KeyResp = resp_device.read(1)
    KeyPressTime = timer.getTime()
    if len(KeyResp) == 0:
        KeyResp = None
        KeyPressTime = np.nan
    else:
        # Map button numbers to side
        ## Blue == 1, Green == 3
        if KeyResp in ['1', '3']:
            KeyResp = 'left'
        elif KeyResp in ['2', '4']:
            KeyResp = 'right'
    return KeyResp, KeyPressTime
