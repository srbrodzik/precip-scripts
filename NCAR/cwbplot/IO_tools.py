import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import re

###reading GRADS data
#grads_dir='/IFS6/data2/datawrf/p108/QPESUMS/data/QPE_2D_2019012812.dat'
compress_dir='/IFS6/data2/datawrf/p108/QPESUMS/rerun_casedata/raincase_o/COMPREF.20181115.0700.gz'
#compress_dir='/IFS6/data2/datarfs/c164/test_data/radar/MREF/MREF3D30L.20200212.0100'
#def QPE_2D_READ(fname):
class QPE_2D_READ:
  def __init__(self,fname):
    data=np.fromfile(fname,dtype='>f',count=-1,sep="")
    self.time_str=re.split('QPE_2D_|.dat',fname)[-2]
    self.datetime=dt.datetime.strptime(self.time_str,"%Y%m%d%H")
    self.nx=441
    self.ny=561
    self.ll_lon=118
    self.ll_lat=20
    self.grid_step=0.0125
    self.undef=-999.
    self.lon_1d = self.ll_lon+np.arange(0,self.nx)*self.grid_step
    self.lat_1d = self.ll_lat+np.arange(0,self.ny)*self.grid_step
    self.lat, self.lon= np.meshgrid(self.lat_1d,self.lon_1d)
    self.data=np.float32(np.reshape(data, (self.nx,self.ny), order='F'))
    #data[data<=0]=np.NaN
  def __str__(self):
     return "CWB QPE_2D data binaray format("+str(np.dtype('>f').descr)+")\n" \
            "TIME:"+ self.datetime.ctime()+"\n" \
            "DIMX,DIMY="+str(self.nx)+','+str(self.ny)+"\n" 
  def __call__(self):
      return self.data
  @classmethod  
  def cwbcolorbar(self):  
    from matplotlib.colors import ListedColormap
    from matplotlib.colors import BoundaryNorm
    rain_color  =["#fdfdfd","#ccccb3","#99ffff","#66b3ff","#0073e6","#002699",\
                  "#009900","#1aff1a","#ffff00","#ffcc00","#ff9900","#ff0000",\
                  "#cc0000","#990000","#800040","#b30047","#ff0066","#ff80b3"]
    rain_colormap = ListedColormap(rain_color)
    clevel=[0,1,2,6,10,15,20,30,40,50,60,70,80,90,110,130,150,200]
    norm=BoundaryNorm(clevel,len(clevel))
    dict({'levels':clevel,'norm':norm,'cmap':rain_colormap})
     
    return  dict({'levels':clevel,'norm':norm,'cmap':rain_colormap})
class COMPREF_READ:
  def __init__(self,fname):
    import struct
    if '.gz' in fname:
        import gzip
        print('unzip files')
        fid = gzip.open(fname).read()
    else:
        fid = open(fname,"rb").read()
    ## Reading time info    
    info=np.array(struct.unpack('<9i4s10i',fid[0:80]))
    self.yyyy=int(info[0])
    self.mm=  int(info[1])
    self.dd=  int(info[2])
    self.hh=  int(info[3])
    self.mn=  int(info[4])
    self.ss=  int(info[5])
    self.nx=  int(info[6])
    self.ny=  int(info[7])
    self.nz=  int(info[8])
    self.time_str=str(self.yyyy)+str(self.mm).zfill(2)+str(self.dd).zfill(2)+str(self.hh).zfill(2)\
                       +str(self.mn).zfill(2)+str(self.ss).zfill(2)
    self.datetime=dt.datetime.strptime(self.time_str,"%Y%m%d%H%M%S")
    ## Reading map projection and grid scale                   
    self.proj=info[9]
    self.map_scale= int(info[10])
    self.projlat1 = int(info[11])
    self.projlat2 = int(info[12])
    self.projlon  = int(info[13])
    self.alon     = int(info[14])
    self.alat     = int(info[15])
    self.xy_scale = int(info[16])
    self.dx       = int(info[17])
    self.dy       = int(info[18])
    self.dxy_scale= int(info[19])
    info=np.array(struct.unpack('<'+str(self.nz+11)+'i20s6s3i',fid[80:80+(self.nz+14)*4+26]))
    next_ind=80+self.nz*4
    self.zht=np.array(struct.unpack('<'+str(self.nz)+'i',fid[80:next_ind])).astype(np.float32)
    info=np.array(struct.unpack('<11i20s6s3i',fid[next_ind:next_ind+14*4+26]))
    self.z_scale=int(info[0])
    self.i_bb_mode=int(info[1])
    self.unkn01=np.array(info[2:10]).astype(np.float32)
    ## Reading data
    self.varname=str(info[11],'utf-8','ignore').replace('\x00','')
    self.varunit=str(info[12],'utf-8','ignore').replace('\x00','')
    self.var_scale= int(info[13])
    self.missing  = int(info[14])
    self.nradar   = int(info[15])
    next_ind=next_ind+14*4+26
    self.mosradar=re.findall('....',(str(struct.unpack('<'+str(self.nradar*4)+'s', \
                  fid[next_ind:next_ind+self.nradar*4])[0],'utf-8','ignore')))
    data_int = struct.unpack(self.nx*self.ny*self.nz*'h', fid[-self.nx*self.ny*self.nz*2:])
    data=np.array(data_int).astype(np.float32)/self.var_scale

    if '30L' in fname:
      self.file_type='mosaicked refl RWRF'
      self.lon, self.lat = np.load('/home/c052/Pub/anaconda3/envs/plotenv/lib/python3.6/site-packages/cwbplot/sharedata/MREF_lonlat.npy')
    else:  
      if 'CREF' in self.varname:
         self.file_type='CREF'                                       
      elif 'CB' in self.varname:
         self.file_type='QPE'                                       
      elif 'mosaicked refl' in self.varname:
         self.file_type='mosaicked refl'
                                                                    ## (alon,alat)     (alon+dlon,alat)  
      self.ll_lon=self.alon/self.xy_scale                           ##      +---------------+
      self.ur_lat=self.alat/self.xy_scale                           ##      |               |
      self.ur_lon=self.ll_lon+self.dx/self.dxy_scale*(self.nx-1)    ##      |               |  alon=dy/dxy*(ny-1)
      self.ll_lat=self.ur_lat-self.dy/self.dxy_scale*(self.ny-1)    ##      |               |  alat=dx/dxy*(nx-1)
      self.lon_1d = np.linspace(self.ll_lon, self.ur_lon, self.nx)  ##      |               |
      self.lat_1d = np.linspace(self.ll_lat, self.ur_lat, self.ny)  ##      |               |
      self.lat, self.lon= np.meshgrid(self.lat_1d,self.lon_1d)      ##      +---------------+
                                                                    ## (alon,alt-dlat)  (alon+dlon,alat-dlat)   
    if self.nz>1 :
       self.data=(np.reshape(data, (self.nx,self.ny,self.nz), order='F'))
    else:   
       self.data=(np.reshape(data, (self.nx,self.ny), order='F'))

  def __str__(self):
     return "CWB "+self.file_type+" binary format("+str(np.dtype('h').descr)+")\n" \
            "TIME:"+ self.datetime.ctime()+"\n" \
            "DIMX,DIMY,DIMZ="+str(self.nx)+','+str(self.ny)+','+str(self.nz)+"\n" 
  def __call__(self):
      return self.data
  def cwbcolorbar(self):  
    from matplotlib.colors import ListedColormap
    from matplotlib.colors import BoundaryNorm
    if  any( x in self.file_type for x in ["REF","ref"]):
      radar_color =["#84C1FF","#2894FF","#0066CC","#28FF28","#00BB00","#009100",\
                    "#F9F900","#FF8000","#FF5151","#EA0000","#AE0000","#FF44FF",\
                    "#D200D2","#750075"]
      radar_colormap = ListedColormap(radar_color)
      clevel =[5,10,15,20,25,30,35,40,45,50,55,60,65,70,75]
      norm=BoundaryNorm(clevel,len(clevel))
      dict({'levels':clevel,'norm':norm,'cmap':radar_colormap})
       
      return  dict({'levels':clevel,'norm':norm,'cmap':radar_colormap})
    
    elif 'QPE' in self.file_type:
      rain_color  =["#fdfdfd","#ccccb3","#99ffff","#66b3ff","#0073e6","#002699",\
                    "#009900","#1aff1a","#ffff00","#ffcc00","#ff9900","#ff0000",\
                    "#cc0000","#990000","#800040","#b30047","#ff0066","#ff80b3"]
      rain_colormap = ListedColormap(rain_color)
      clevel=[0,1,2,6,10,15,20,30,40,50,60,70,80,90,110,130,150,200]
      norm=BoundaryNorm(clevel,len(clevel))
      dict({'levels':clevel,'norm':norm,'cmap':rain_colormap})
       
      return  dict({'levels':clevel,'norm':norm,'cmap':rain_colormap})
class DOPPLER_3D_READ:
  def __init__(self,fname):
    import struct
    if '.gz' in fname:
        import gzip
        print('unzip files')
        fid = gzip.open(fname).read()
    else:
        fid = open(fname,"rb").read()
    
    self.nx=441
    self.ny=561
    self.nz=10
    self.ll_lon=118
    self.ll_lat=20
    self.grid_step=0.0125
    self.undef=-99.
    self.lon_1d = self.ll_lon+np.arange(0,self.nx)*self.grid_step
    self.lat_1d = self.ll_lat+np.arange(0,self.ny)*self.grid_step
    self.lat, self.lon= np.meshgrid(self.lat_1d,self.lon_1d)
    record = np.array(struct.unpack('<4948060f', fid))  ### Every fortran unformatted data has 4 bytes header and tailing
    index = np.where(abs(record) <=1.38673057e-39)        ### The header and tailing encode to float32 are small number 10^(-39)
    data = np.delete(record, index)
    data[np.where(data==self.undef)] = float('nan')
    data_3d = np.reshape(data,(441,561,-1), order='F')
    self.data_u = data_3d[:,:,::2]
    self.data_v = data_3d[:,:,1::2]
class MSC_READ:
   def __init__(self,fname):
     import numpy as np
     self.data=dict()
     gispath='cwbplot/sharedata/'
     file_proj={1350:gispath+'Proj_Python_Scale005_1350x1350',
                2750:gispath+'Proj_Python_Scale050_2750x2750'}
     data_type={'ALB':'f','CNT':'uint8','BTP':'f'}
     ### ingest data
     if '.gz' in fname:
         self.res=int(fname.split('.')[-3])
         self.band=fname.split('.')[-4]
         self.area=fname.split('.')[-5]   
         import tarfile
         file=tarfile.open(fname, "r:gz")   
         for member in file:
           print(member)
           var_name=member.name.split('.')[-1].upper()
           array=np.frombuffer(file.extractfile(member).read(),dtype=data_type[var_name]) 
           self.data[self.band+'_'+var_name] =  np.reshape(array,(self.res,self.res), order='C')

     else:       
         self.res=int(fname.split('.')[-2])  
         self.band=fname.split('.')[-3]
         self.area=fname.split('.')[-4]    
         var_name=fname.split('.')[-1].upper()
         array = np.fromfile(fname,dtype=data_type[var_name],count=-1,sep="")
         self.data[self.band+'_'+var_name] =  np.reshape(array,(self.res,self.res), order='C')
    ## Ingest projection info
     array_proj=np.fromfile(file_proj[self.res],dtype='f',count=-1,sep="")
     lat,lon =array_proj[0:self.res**2],array_proj[-self.res**2:]
     self.lon = np.reshape(lon, (self.res,self.res), order='C')
     self.lat = np.reshape(lat, (self.res,self.res), order='C')   
    
