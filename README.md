A crappy library for efficiently reading large TDMS files with and without index files, based on pyTDMS.

Why does this library exist? Have tried nptdms and pytdms to read in TDMS files. Results:
  - TDMS format only allows efficient seeking/random access in large files if there is a correspondig .tdms_index file
  - if no index file is present, objects in a file can be iterated through, but it is not possible to know in advance how many objects are in the file
  - nptmds has support for index files, but runs into memory problems for very large files
  - pytdms does not support index files

This module provides two fast ways to read in TDMS files (though without support for multi-segment objects), building on pytdms.

First way is with index file (`read_index` and `get_object` functions; convenience functions `groups`, `channels_count`).

Example: 
  ```
  import crappytdms
  idx = crappytdms.read_index("bla.tdms_index")
  print("groups: ", crappytdms.groups(idx))
  print("channels in group1: ", crappytdms.channels_count(idx, b"'group1'"))
  data = crappytdms.get_object("bla.tdms", idx, b"/'group1'/'15'")
  ```

Second way is without index file (`iterate` function).

Example:
  ```
  for name, data in crappytdms.iterate("bla.tdms"):
    print(name, data.shape)
  ```

LICENSE: GPL 2.0 (inherited from pytdms).

Can be installed with pip:

  ```
  pip3 install git+https://gitlab.com/leberwurscht/crappytdms.git
  ```
