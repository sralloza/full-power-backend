# HealthData algorithm examples

## Inputs

*If you enter these inputs in the excel file:*

```default
0 4 4 3 4 2 2 0 3 2 4 0 0 4 4 3 2 1 3
2 0 1 1 0 1 4 4 4 0 0 4 4 4 4 4 4 4 4
1 4 2 1 3 0 4 0 4 4 4 2 3 2 3 1 0 2 4
2 4 3 1 4 0 1 2 0 4 0 3 0 1 0 2 3 4 2
```

!!! note "Explanation of the inputs"
    **Each line represents a different input.** The numbers in the columns are the values you need to put in the excel.

    For example, the first value of the first input (`0`) corresponds to the first question (*What's your energy?*), the second value of the first input (`4`) corresponds to the second question (*Do you have a restful sleep?*) and so on.

!!! note
    In the excel, you need to **put** the questions answers in the column `D`, rows from `6` to `24`.

## Outputs

*You should see these outputs:*

|vitamins|sleep|diet|stress|
|:--:|:--:|:--:|:--:|
|0.50000|0.12500|0.29167|0.37500|
|0.47917|0.87500|0.00000|0.50000|
|0.39583|0.41667|0.50000|0.04167|
|0.58333|0.33333|0.50000|0.79167|

!!! note "Explanation of the outputs"
    **Each line is a different output.** The first value is the output from the first problem (*vitamins*), the second value is the output from the second problem (*sleep*), and so on. It it a value from `0` to `1`, being `1` the **worst**.

!!! note
    In the excel, you can **see** the outputs on line `30`, columns `F`, `H`, `J` and `L`.

## Other info

If you are looking for the links of Stephane's excel, you will find them on the previous section ([HealthData algorithm explanation](hd-algorithm.md))
