
import logging
logger = logging.getLogger(__name__)

import pyopencl

from gputools import get_device

class CL_BUILD_PROGRAM_FAILURE:
    pass


class OCLProgram(pyopencl.Program):
    """ a wrapper class representing a CPU/GPU Program

    example:

         prog = OCLProgram("mykernels.cl",build_options=["-D FLAG"])
    
    """

    def __init__(self,file_name = None,src_str = None, build_options =[], dev = None):
        if file_name is not None:
            with open(file_name,"r") as f:
                src_str = f.read()
                
        if src_str is None:
            raise ValueError("empty src_str! ")

        if dev is None:
            dev = get_device()
        self.dev = dev
        super(OCLProgram,self).__init__(self.dev.context,src_str)
        self.build(options = build_options)

    def run_kernel(self, name, global_size, local_size,*args,**kwargs):
        getattr(self,name)(self.dev.queue,global_size, local_size,*args,**kwargs)




if __name__ == '__main__':
    import numpy as np
    from gputools import OCLArray
    
    s =    """
    __kernel void add(__global float *a_g, float val){

    int i = get_global_id(0);
    a_g[i] += val;

    }
    """

    prog = OCLProgram(src_str = s)

    d = np.random.rand(1000).astype(np.float32) 
    b = OCLArray.from_array(d)

    prog.run_kernel("add",b.shape,None,b.data,np.float32(2.))

