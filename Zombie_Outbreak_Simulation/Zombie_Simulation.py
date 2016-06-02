
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import numpy as np
import moviepy.editor as mpy

usa = mpy.ImageClip("usa_density.png")
SIR = np.zeros((3, usa.h, usa.w)).astype(np.float)
SIR[0] = usa.get_frame(0) / 255
