import numpy as np

empty_ = np.array(
        0,
        dtype=[
            ("Position", np.float32),
            ("Cost", np.float32),
            ("Objetive", np.float32),
            ("IsDominated", np.float32),
            ]
    )
empty_["Position"] = 1
x = np.array(empty_)
print(empty_)
print(x)
