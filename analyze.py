# Simple MSAF example
from __future__ import print_function
import msaf
import numpy as np

# 1. Select audio file
audio_file = "audio\\AUDIO_6821.mp3"

print("features:", msaf.features_registry)
print("boundary:", msaf.get_all_boundary_algorithms())
print("label:", msaf.get_all_label_algorithms())

# 2. Segment the file using the default MSAF parameters (this might take a few seconds)
boundaries, labels = msaf.process(audio_file, feature='mfcc',
                                  boundaries_id = 'cnmf',plot=True)
print('feature: mfcc')
print('Estimated boundaries:', boundaries)
print('Estimated labels:', labels)

# 3. Save segments using the MIREX format
out_file = 'segments.txt'
print('Saving output to %s' % out_file)
msaf.io.write_mirex(boundaries, labels, out_file)