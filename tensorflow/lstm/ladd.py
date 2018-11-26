import  numpy



def sigmoid(x):
    return 1./(1+numpy.exp(x))

def sigmoid_output_dervitive(output):
    return output*(1-output)

def random_arr(a,b,*args):
    numpy.random.seed(0)
    return numpy.random.rand(*args)*(b-a)+a

class LstmParam:
    def __init__(self,mem_cell_ct,x_dim):
        self.mem_cell_ct=mem_cell_ct
        self.x_dim=x_dim
        concat_len=x_dim+mem_cell_ct

        #weight matrices
        self.wg=random_arr(-0.1,0.1,mem_cell_ct,concat_len)
        self.wi=random_arr(-0.1,0.1,mem_cell_ct,concat_len)
        self.wf=random_arr(-0.1,0.1,mem_cell_ct,concat_len)
        self.wo=random_arr(-0.1,0.1,mem_cell_ct,concat_len)

        #bias terms
        self.bg=random_arr(-0.1,0.1,mem_cell_ct)
        self.bi=random_arr(-0.1,0.1,mem_cell_ct)
        self.bf=random_arr(-0.1,0.1,mem_cell_ct)
        self.bo=random_arr(-0.1,0.1,mem_cell_ct)

        #diffs
        self.wg_diff=numpy.zeros((mem_cell_ct,concat_len))
        self.wi_diff=numpy.zeros((mem_cell_ct,concat_len))
        self.wf_diff=numpy.zeros((mem_cell_ct,concat_len))
        self.wo_diff=numpy.zeros((mem_cell_ct,concat_len))

        self.bg_diff=numpy.zeros(mem_cell_ct)
        self.bi_diff=numpy.zeros(mem_cell_ct)
        self.bf_diff=numpy.zeros(mem_cell_ct)
        self.bo_diff=numpy.zeros(mem_cell_ct)

    def apply_diff(self,lr=1):
        self.wg -=lr*self.wg_diff
        self.wi -=lr*self.wi_diff
        self.wf -=lr*self.wf_diff
        self.wo -=lr*self.wo_diff

        self.bg -=lr*self.bg_diff
        self.bi -=lr*self.bi_diff
        self.bf -=lr*self.bf_diff
        self.bo -=lr*self.bo_diff

        #reset diffs to zero
        self.wg_diff=numpy.zeros_like(self.wg)
        self.wi_diff=numpy.zeros_like(self.wi)
        self.wf_diff=numpy.zeros_like(self.wf)
        self.wo_diff=numpy.zeros_like(self.wo)

        self.bg_diff=numpy.zeros_like(self.bg)
        self.bi_diff=numpy.zeros_like(self.bi)
        self.bf_diff=numpy.zeros_like(self.bf)
        self.bo_diff=numpy.zeros_like(self.bo)

class LstmState:
    def __init__(self,mem_cell_ct,x_dim):
        self.g = numpy.zeros(mem_cell_ct)
        self.i = numpy.zeros(mem_cell_ct)
        self.f= numpy.zeros(mem_cell_ct)
        self.o= numpy.zeros(mem_cell_ct)
        self.s= numpy.zeros(mem_cell_ct)
        self.h= numpy.zeros(mem_cell_ct)

        self.bottom_diff_h=numpy.zeros(self.h)
        self.bottom_diff_s=numpy.zeros(self.s)
        self.bottom_diff_x=numpy.zeros(x_dim)

class LstmNode:
    def __init__(self,lstm_param,lstm_state):

        self.state=lstm_state
        self.param=lstm_param

        self.x=None
        self.xc=None

    def bottom_data_is(self,x,s_prev=None,h_prev=None):

        if s_prev == None: s_prev = numpy.zeros_like(self.state.s)
        if h_prev == None: h_prev = numpy.zeros_like(self.state.h)

        self.s_prev = s_prev
        self.h_prev = h_prev

        xc= numpy.hstack((x,h_prev))
        self.state.g = numpy.tanh(numpy.dot(self.param.wg,xc)+self.param.bg)
        self.state.i = sigmoid(numpy.dot(self.param.wi,xc)+self.param.bi)
        self.state.f = sigmoid(numpy.dot(self.param.wf,xc)+self.param.bf)
        self.state.o = sigmoid(numpy.dot(self.param.wo,xc)+self.param.bo)
        self.state.s = self.state.g * self.state.i + s_prev * self.state.f
        self.state.h = self.state.s * self.state.o

        self.x = x
        self.xc=xc

    def top_diff_is(self,top_diff_h,top_diff_s):

        ds =self.state.o * top_diff_h+top_diff_s
        do =self.state.s * top_diff_h
        di =self.state.g * ds
        dg =self.state.i * ds
        df =self.s_prev * ds

        di_input =(1. - self.state.i) * self.state.i *di
        df_input =(1. - self.state.f) * self.state.f *df
        do_input =(1. - self.state.o) * self.state.o *do
        dg_input =(1. - self.state.g ** 2 ) *dg

        self.param.wi_diff += numpy.outer(di_input,self.xc)
        self.param.wf_diff += numpy.outer(df_input,self.xc)
        self.param.wo_diff += numpy.outer(do_input,self.xc)
        self.param.wg_diff += numpy.outer(dg_input,self.xc)

        self.param.bi_diff +=di_input
        self.param.bf_diff +=df_input
        self.param.bo_diff +=do_input
        self.param.bg_diff +=dg_input

        dxc = numpy.zeros(self.xc)
        dxc += numpy.dot(self.param.wi.T,di_input)
        dxc += numpy.dot(self.param.wf.T,df_input)
        dxc += numpy.dot(self.param.wo.T,do_input)
        dxc += numpy.dot(self.param.wg.T,dg_input)

        self.state.bottom_diff_s = ds * self.state.f
        self.state.bottom_diff_x = dxc[:self.param.x_dim]
        self.state.bottom_diff_h = dxc[self.param.x_dim:]

        #33第二个例子










