import struct

import numpy as np
import pytdms

def readLeadIn_index(f):
    """
    Helper function for read_index.

    Read the lead-in of a tdms-index file segment.
    Copied from pytdms, but replaced 'TDSm' by 'TDSh'.
    """

    s = f.read(4) # read 4 bytes
    if (not s in [b'TDSh']):
        print("Error: segment does not start with TDSh, but with ", s)
        exit()
    s = f.read(4)
    toc = struct.unpack("<i", s)[0]
    metadata = {}
    for prop in pytdms.tocProperties.keys():
        metadata[prop] = (toc & pytdms.tocProperties[prop])!=0

    s = f.read(4)
    version = struct.unpack("<i", s)[0]
    s = f.read(16)
    (next_segment_offset,raw_data_offset) = struct.unpack("<QQ", s)
    return (metadata,version,next_segment_offset,raw_data_offset)

def read_index(filename):
  """
    reads in tdms-index file for use with channels_count, groups, get_object.
    returns a dict with the segment's offset in the file for each object of the tdms file.
    (compare also https://gist.github.com/flocke/1c6adc38c7b0191245017946a891debf)
  """

  filesize = os.path.getsize(filename)
  f = open(filename,"rb")

  i=0
  largefileoffset = 0
  idx = {}
  while f.tell()<filesize:
    offset = f.tell()
    metadata,version,next_segment_offset,raw_data_offset = readLeadIn_index(f)
    if (metadata["kTocMetaData"]):
      obj,_ = pytdms.readMetaData(f)
      for k,v in obj.items():
        if k in idx: raise NotImplementedError("multi-segment objects not implemented")
        idx[k] = largefileoffset
    largefileoffset += next_segment_offset + 7*4

    if i%1000==0:
      print("reading index... ", offset/filesize/1e-2,"%")

    i+=1

  return idx

def groups(idx):
  """
    Lists all groups in the TDMS file.
    Example: print(groups(idx))
  """
  groups = []
  for k,v in idx.items():
    if b'/' not in k[1:] and not k==b"/": groups.append(k[1:])
  return groups

def channels_count(idx, group):
  """
    Counts the channels in a group.
    Example: print(channels_count(idx, b"'group1'"))
  """
  l = 0
  for k,v in idx.items():
    if k.startswith(b"/"+group+b"/"):
      l+=1
  return l

def get_object(f, idx, path):
  """
    Get raw data for one object of the TDMS file.
    Example: 
      idx = read_index("bla.tdms_index")
      data = get_object("bla.tdms", idx, b"/'group1'/'15'")
  """
  if type(f)==str: f = open(f,"rb")
  filesize = os.fstat(f.fileno()).st_size

  f.seek(idx[path])
  objects, rawdata = pytdms.readSegment(f, filesize, ({},{}))
  return np.asarray(rawdata[path])

def iterate(f, startpos=0):
  """
    Yields pairs of object name and object raw data in a TDMS file.
    Works without index, but you won't know number of objects in advance.

    Example:
      for name, data in iterate("bla.tdms"):
        print(name, data.shape)
  """

  if type(f)==str: f = open(f,"rb")
  #filesize = os.fstat(f.fileno()).st_size
  f.seek(0,2); filesize=f.tell(); f.seek(0)

  #t = time.time()
  pos = startpos
  while pos<filesize:
    #print(pos/1e9, "GB", pos/1e6/(time.time()-t), "MB/s")
    objects, rawdata = pytdms.readSegment(f, filesize, ({},{}))
    for k,v in rawdata.items(): yield pos, k, np.asarray(v)
    pos = f.tell()
