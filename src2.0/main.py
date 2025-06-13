NetworkChecker = type(
    "NetworkChecker",
    (object,),
    {
        "is_valid_ip": lambda self, ip, v6=False: bool(
            __import__("re").search(
                r"^([0-9A-F]{4}:?){8}$"
                if v6
                else r"^((25[0-5]|(2[0-4]|1\d|[1-9]?|)\d)\.?\b){4}$",
                ip.upper(),
            )
        ),
        "is_valid_mac": lambda self, mac: bool(
            __import__("re").search(r"^([0-9A-F]{2}:?){6}$", mac.upper())
        ),
    },
)
print(NetworkChecker().is_valid_ip("2001:0DB8:85A3:0000:0000:8A2E:0370:7334", v6=True)),print(NetworkChecker().is_valid_mac("A1:B2:C3:DD:5F:6F")),print(NetworkChecker().is_valid_ip("255.255.255.255", v6=False))  # fmt: off

type Vector = list[float]
