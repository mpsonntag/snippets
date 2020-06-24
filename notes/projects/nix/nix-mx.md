------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

nix-mx: Support doByEntity

LEAVE THIS FOR A LATER TIME; WHEN IT HAS BEEN DECIDED HOW LOOKUP SHOULD WORK IN NIX

Depends whether this actually makes sense - if its not significantly faster doing this in the backend
I would be for leaving these out to reduce the number of functions that do stuff and make it easier on the user.

File
-[ ] hasBlock(Block)
-[ ] deleteBlock(Block)
-[ ] hasSection(Section)
-[ ] deleteSection(Section)

Block
-[ ] hasSource(Source)
-[ ] deleteSource(Source)
-[ ] hasDataArray(DataArray)
-[ ] deleteDataArray(DataArray)
-[ ] hasTag(Tag)
-[ ] deleteTag(Tag)
-[ ] hasMultiTag(Tag)
-[ ] deleteMultiTag(MultiTag)
-[ ] hasGroup(Group)
-[ ] deleteGroup(Group)
-[ ] metadata(Section)

Group
-[ ] hasDataArray(DataArray)
-[ ] addDataArray(DataArray)
-[ ] removeDataArray(DataArray)
-[ ] hasTag(Tag)
-[ ] addTag(Tag)
-[ ] removeTag(Tag)
-[ ] hasMultiTag(MultiTag)
-[ ] addMultiTag(MultiTag)
-[ ] removeMultiTag(MultiTag)
-[ ] metadata(Section)
-[ ] hasSource(Source)
-[ ] addSource(Source)
-[ ] removeSource(Source)

DataArray
-[ ] metadata(Section)
-[ ] hasSource(Source)
-[ ] addSource(Source)
-[ ] removeSource(Source)

Source
-[ ] hasSource(Source)
-[ ] deleteSource(Source)
-[ ] metadata(Section)

Tag
-[ ] hasReference(DataArray)
-[ ] addReference(DataArray)
-[ ] removeReference(DataArray)
-[ ] hasFeature(Feature)
-[ ] createFeature(DataArray, LinkType)
-[ ] deleteFeature(Feature)
-[ ] metadata(Section)
-[ ] hasSource(Source)
-[ ] addSource(Source)
-[ ] removeSource(Source)

MultiTag
-[ ] positions(DataArray)
-[ ] extents(DataArray)
-[ ] hasReference(DataArray)
-[ ] addReference(DataArray)
-[ ] removeReference(DataArray)
-[ ] hasFeature(Feature)
-[ ] createFeature(DataArray, LinkType)
-[ ] deleteFeature(Feature)
-[ ] metadata(Section)
-[ ] hasSource(Source)
-[ ] addSource(Source)
-[ ] removeSource(Source)

Feature
-[ ] data(DataArray)

Section
-[ ] link(Section)
-[ ] hasSection(Section)
-[ ] deleteSection(Section)
-[ ] hasProperty(Property)
-[ ] deleteProperty(Property)

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

Add getIndex function to dimensions

-[ ] SetDimension
-[ ] RangeDimension
-[ ] SampledDimension


ToDo
- add LinkType to Schema!
- update Model in wiki + model to description
- add all Models to doc

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

nix-mx proper multitag test

    f = nix.File(fullfile(pwd, 'tests', 'testRW.h5'), nix.FileMode.Overwrite);
    b = f.create_block('testBlock', 'nixBlock');

    % starting positions y, x and extents y+n, x+m of three tags for 2D data
    pos(1,:) = [0, 0]; ext(1,:) = [0, 0]; % result 111
    
    pos(2,:) = [0, 3]; ext(2,:) = [0, 2]; % result 114, 115
    
    pos(3,:) = [1, 1]; ext(3,:) = [0, 3]; % result 122 123 124
    
    pos(4,:) = [0, 2]; ext(4,:) = [2, 4];   % result 113 114 115 116
                                            %        123 124 125 126
    pos(5,:) = [0, 0]; ext(5,:) = [0, 10]; % fail due to too large extent in x
    
    pos(6,:) = [0, 0]; ext(6,:) = [3, 0]; % fail due to too large extent in y
    
    d_pos = b.create_data_array_from_data('positionsDA', 'nixDataArray', pos);
    d_pos.append_sampled_dimension(0);
    d_pos.append_sampled_dimension(0);

    d_ext = b.create_data_array_from_data('extentsDA', 'nixDataArray', ext);
    d_ext.append_sampled_dimension(0);
    d_ext.append_sampled_dimension(0);

    % create multi tag with the data array containing the three 
    % starting positions of the tags.
    t = b.create_multi_tag('testMultiTag', 'nixMultiTag', d_pos);
    % adding the extents of the three tags.
    t.set_extents(d_ext);

    % create 2D reference data_arrays
    raw1 = [111, 112, 113, 114, 115, 116, 117, 118; ...
                121, 122, 123, 124, 125, 126, 127, 128];
    d1 = b.create_data_array_from_data('reference1', 'nixDataArray', raw1);
    dim_y = d1.append_sampled_dimension(1);
    dim_y.label = 'y1';
    dim_x = d1.append_sampled_dimension(1);
    dim_x.label = 'x1';

    raw2 = [211, 212, 213, 214, 215, 216, 217, 218; ...
                221, 222, 223, 224, 225, 226, 227, 228];
    d2 = b.create_data_array_from_data('reference2', 'nixDataArray', raw2);
    dim_y = d2.append_sampled_dimension(1);
    dim_y.label = 'y2';
    dim_x = d2.append_sampled_dimension(1);
    dim_x.label = 'x2';

    % add data_arrays as references to multi tag
    t.add_reference(d1);
    t.add_reference(d2);

    % test invalid position idx
    try
        t.retrieve_data_idx(100, 0);
    catch ME
        assert(~isempty(strfind(ME.message, 'ounds of positions or extents')), ...
            'Invalid position index failed');
    end

    % test invalid reference idx
    try
        t.retrieve_data_idx(0, 100);
    catch ME
        assert(~isempty(strfind(ME.message, 'out of bounds')), ...
            'Invalid reference index failed');
    end
    
    % test retrieving data for first position, first reference
    disp(t.retrieve_data_idx(0, 0))

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

- nix/nix-mx: static linux build
    currently fails:

        /usr/bin/c++ -fPIC -std=c++11 -Wall -pedantic -Wunreachable-code  -shared -Wl,-soname,nix_mx.mexa64.1 -o nix_mx.mexa64.1.4.0 CMakeFiles/nix_mx.dir/nix_mx.cc.o CMakeFiles/nix_mx.dir/src/nixblock.cc.o CMakeFiles/nix_mx.dir/src/nixdataarray.cc.o CMakeFiles/nix_mx.dir/src/nixdimensions.cc.o CMakeFiles/nix_mx.dir/src/nixfeature.cc.o CMakeFiles/nix_mx.dir/src/nixfile.cc.o CMakeFiles/nix_mx.dir/src/nixgroup.cc.o CMakeFiles/nix_mx.dir/src/nixmultitag.cc.o CMakeFiles/nix_mx.dir/src/nixproperty.cc.o CMakeFiles/nix_mx.dir/src/nixsection.cc.o CMakeFiles/nix_mx.dir/src/nixsource.cc.o CMakeFiles/nix_mx.dir/src/nixtag.cc.o CMakeFiles/nix_mx.dir/src/utils/mkarray.cc.o CMakeFiles/nix_mx.dir/src/utils/mknix.cc.o  -L/home/msonntag/Chaos/software/Matlab/matlabRoot/bin/glnxa64 -Wl,-rpath,/home/msonntag/Chaos/software/Matlab/matlabRoot/bin/glnxa64 -lmex -lmx -leng /usr/local/lib/libnix.a -Wl,-Bstatic -lboost_date_time -lboost_regex -lboost_program_options -lboost_system -lboost_filesystem -Wl,-Bdynamic /usr/lib/x86_64-linux-gnu/hdf5/serial/libhdf5.a -lpthread -lsz -lz -ldl -lm 

        /usr/bin/ld: /usr/lib/gcc/x86_64-linux-gnu/5/../../../x86_64-linux-gnu/libboost_date_time.a(greg_month.o): relocation R_X86_64_32S against `.rodata' can not be used when making a shared object; recompile with -fPIC

        /usr/lib/gcc/x86_64-linux-gnu/5/../../../x86_64-linux-gnu/libboost_date_time.a: error adding symbols: Bad value

        collect2: error: ld returned 1 exit status


    - changes in nix/cmakelist.txt


    - changes in nix-mx/cmakelist.txt

            cmake_minimum_required(VERSION 2.8.4)
            project(nix_mx CXX C) # changed for nix-mx static build
            
            set(VERSION_MAJOR 1)
            set(VERSION_MINOR 4)
            set(VERSION_PATCH 0)
            
            set(VERSION_ABI   1)
            
            set(CMAKE_VERBOSE_MAKEFILE TRUE) # changed for nix-mx static build
            
            ### include local modules
            set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake")
            
            if(NOT WIN32)
              set(CMAKE_CXX_FLAGS "-fPIC") # changed for nix-mx static build

    - changes in nix-mx/cmake/findMatlab.cmake

              # Get path to the include directory
              FIND_PATH(MATLAB_INCLUDE_DIR
                "mex.h"
                "${MATLAB_ROOT}/extern/include"
                )
            ELSE(WIN32)
              SET(MATLAB_ROOT "/home/msonntag/Chaos/software/Matlab/matlabRoot/")

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

- nix-mx: now that it is static, try to build for linux
- nix-mx: remove huge test file
- nix-mx: setting up Matlab on mac
- nix-mx: get Matlab version 2017
- nix-mx: allow non-SI units in Properties and DataArrays (vgl. https://github.com/G-Node/nixpy/pull/281)
