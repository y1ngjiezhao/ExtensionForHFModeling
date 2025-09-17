
In this project, we focus on the levels 10 to 12 (we tried other levels, in decision parts, BU_IR shows terrible performance).
If you want to reproduce the data processing, you could only choose the last 3 elements (from 10 to 12), as follows.
  SPEC_LVLS_1_TO_12 = [
      ["total", "cat_id", "dept_id", "item_id"],    # Level 10
      ["total", "state_id", "cat_id", "dept_id", "item_id"],   # Level 11
      ["total", "state_id", "store_id", "cat_id", "dept_id", "item_id"]   # Most disaggregated level (lvl 12)
  ]

And other .py files are focusing on different parts for the whole data frame (lags, prices, ...).

If there are still confusion, feel free to contact yingjie.zhao@hdr.qut.edu.au
