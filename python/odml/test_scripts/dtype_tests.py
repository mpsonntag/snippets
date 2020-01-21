import odml
import datetime as dt

# basic types
prop_i = odml.Property(name="int", value=[1, 2, 3])
prop_f = odml.Property(name="float", value=[1.0, 2.0, 3.0])
prop_b = odml.Property(name="bool", value=[True, False, False])

# check fails
odml.dtypes.get("bla", prop_i.dtype)
odml.dtypes.get("bla", prop_f.dtype)
odml.dtypes.get("bla", prop_b.dtype)

# date time types
prop_d = odml.Property(name="date", dtype=odml.dtypes.DType.date, value=["2019-12-12"])
prop_t = odml.Property(name="time", dtype=odml.dtypes.DType.time, value=["12:12:12"])
prop_dt = odml.Property(name="datetime", dtype=odml.dtypes.DType.datetime,
                        value=["2019-12-12 12:12:12"])

# check fails
odml.dtypes.get("bla", prop_d.dtype)
odml.dtypes.get("bla", prop_t.dtype)
odml.dtypes.get("bla", prop_dt.dtype)

# string based types will accept everything
