COMMITS = {
    "13dd3de199a7ed06fbab98ba479cc2fbb7f83875": [
        ("myapp", "0002_mymodel_tz_created"),
        ("myapp", "0003_mymodel_is_active"),
        ("myapp", "0003_mymodel_is_paid"),
        ("myapp", "0004_merge_20200502_0148"),
        ("myapp", "0005_auto_20200502_0149"),
    ],
    "bfcc26981425aedeb098229a19ec91011519dabf": [
        ("myapp", "0003_mymodel_is_active"),
        ("myapp", "0003_mymodel_is_paid"),
        ("myapp", "0004_merge_20200502_0148"),
        ("myapp", "0005_auto_20200502_0149"),
    ],
    "34e0765cb83905cd53813904941cac32d47f882a": [
        ("myapp", "0003_mymodel_is_active"),
        ("myapp", "0004_merge_20200502_0148"),
        ("myapp", "0005_auto_20200502_0149"),
    ],
    "c1cac76ee4bbca46ee8de58c51bfc70fac38b9a6": [
        ("myapp", "0004_merge_20200502_0148"),
        ("myapp", "0005_auto_20200502_0149"),
    ],
    "59efbed241843a6079b759eb69239ae1434366a9": [("myapp", "0005_auto_20200502_0149")],
    "3d0e74a401521511ab4e58f767661a4bbfedf32a": [],
}

PARENTS = {
    ("myapp", "0005_auto_20200502_0149"): [("myapp", "0004_merge_20200502_0148")],
    ("myapp", "0004_merge_20200502_0148"): [
        ("myapp", "0003_mymodel_is_active"),
        # ("myapp", "0003_mymodel_is_paid"), # This one should be left out due to ordering
    ],
    ("myapp", "0003_mymodel_is_paid"): [("myapp", "0002_mymodel_tz_created")],
    ("myapp", "0003_mymodel_is_active"): [("myapp", "0002_mymodel_tz_created")],
    ("myapp", "0002_mymodel_tz_created"): [("myapp", "0001_initial")],
    ("myapp", "0001_initial"): [("myapp", None)],
}
