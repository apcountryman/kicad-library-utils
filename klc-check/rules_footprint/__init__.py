def get_all_footprint_rules():
    # without this delayed import, the rules could not import our sub-modules (e.g. klc_constants)
    from . import (
        EC01,
        EC02,
        F5_1,
        F5_2,
        F5_3,
        F5_4,
        F6_1,
        F6_2,
        F6_3,
        F7_1,
        F7_2,
        F7_3,
        F7_4,
        F7_5,
        F7_6,
        F9_1,
        F9_2,
        F9_3,
        G1_1,
        G1_7,
    )

    return {
        "EC01": EC01,
        "EC02": EC02,
        "G1.1": G1_1,
        "G1.7": G1_7,
        "F5.1": F5_1,
        "F5.2": F5_2,
        "F5.3": F5_3,
        "F5.4": F5_4,
        "F6.1": F6_1,
        "F6.2": F6_2,
        "F6.3": F6_3,
        "F7.1": F7_1,
        "F7.2": F7_2,
        "F7.3": F7_3,
        "F7.4": F7_4,
        "F7.5": F7_5,
        "F7.6": F7_6,
        "F9.1": F9_1,
        "F9.2": F9_2,
        "F9.3": F9_3,
    }
