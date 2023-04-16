import pandas as pd


def pandas_output_setting():
    """Set pandas _output display setting"""
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", None)
    ##pd.set_option('display.max_columns', 500)
    pd.set_option("display.width", 140)
    pd.set_option("display.max_colwidth", None)
    pd.options.mode.chained_assignment = None  # default='warn'


control_panel = {
    "scrape_every_x_min": 5 * 60,
}

other_discord_channel = {
    "_demo_alert_bayc": 1047374847543627786,
    "_demo_alert_cryptopunksv1": 1047390362794197022,
    "assorted_listing_all_tier": 1048330550919827456,
    "assorted_listing_tier2": 1048330631077171370,
    "assorted_listing_tier1": 1048330677227106345,
}

nft_meta_dict = {
    "bayc": {
        "gem_slug": "boredapeyachtclub",
        "contract": "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D",
        "discord_channel_listing_all_tier": 1048329329144234085,
        "discord_channel_listing_tier2": 1048330050677784646,
        "discord_channel_listing_tier1": 1048330215677493388,
    },
    "mayc": {
        "gem_slug": "mutant-ape-yacht-club",
        "contract": "0x60E4d786628Fea6478F785A6d7e704777c86a7c6",
        "discord_channel_listing_all_tier": 1053366092267016213,
        "discord_channel_listing_tier2": 1053366140224667658,
        "discord_channel_listing_tier1": 1053366179344957470,
    },
    "cryptopunksv1": {
        "gem_slug": "official-v1-punks",
        "contract": "0x282BDD42f4eb70e7A9D9F40c8fEA0825B7f68C5D",
        "discord_channel_listing_all_tier": 1048330718008324148,
        "discord_channel_listing_tier2": 1048330720046760006,
        "discord_channel_listing_tier1": 1048332353111593000,
    },
    "cryptopunks": {
        "gem_slug": "cryptopunks",
        "contract": "0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB",
        "discord_channel_listing_all_tier": 1048332402071715940,
        "discord_channel_listing_tier2": 1048332437991739392,
        "discord_channel_listing_tier1": 1048332471156101181,
    },
    "pridepunks": {
        "gem_slug": "pridepunks2018",
        "contract": "0x0144B7e66993C6BfaB85581e8601f96BFE50c9Df",
        "discord_channel_listing_all_tier": 1061756584591638668,
        "discord_channel_listing_tier2": 1061756620931088404,
        "discord_channel_listing_tier1": 1061756651851481179,
    },
    "cryptoarte": {
        "gem_slug": "cryptoarte",
        "contract": "0xBACe7E22f06554339911A03B8e0aE28203Da9598",
        "discord_channel_listing_all_tier": 1048332504735682622,
        "discord_channel_listing_tier2": 1048332683522093206,
        "discord_channel_listing_tier1": 1048332832902234182,
    },
    "autoglyphs": {
        "gem_slug": "autoglyphs",
        "contract": "0xd4e4078ca3495de5b1d4db434bebc5a986197782",
        "discord_channel_listing_all_tier": None,
        "discord_channel_listing_tier2": None,
        "discord_channel_listing_tier1": None,
    },
    "mooncats": {
        "gem_slug": "acclimatedmooncats",
        "contract": "0xc3f733ca98E0daD0386979Eb96fb1722A1A05E69",
        "discord_channel_listing_all_tier": 1048332875226951680,
        "discord_channel_listing_tier2": 1048332903668514876,
        "discord_channel_listing_tier1": 1048332930960851054,
    },
    "cryptophunks": {
        "gem_slug": "crypto-phunks",
        "contract": "0xf07468eAd8cf26c752C676E43C814FEe9c8CF402",
        "discord_channel_listing_all_tier": 1048332966344003625,
        "discord_channel_listing_tier2": 1048332999676137512,
        "discord_channel_listing_tier1": 1048333037873680405,
    },
    "nftworlds": {
        "gem_slug": "nft-worlds",
        "contract": "0xBD4455dA5929D5639EE098ABFaa3241e9ae111Af",
        "discord_channel_listing_all_tier": 1048339489317212260,
        "discord_channel_listing_tier2": 1048339521978257479,
        "discord_channel_listing_tier1": 1048339559777325147,
    },
}

# `max_rel_flr_price_multiplier` means max relative price, as a price multiplier from floor price; `max_abs_price` is max absolute price
asset_filter_dict = {
    "_generic": [
        {
            "tier": 1,
            "trait_string_any": [],
            "trait_string_all": [],
            "trait_string_not": [],
            "min_rank": None,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 0.5,
            "token_id_any": [],
        },
        {
            "tier": 1,
            "trait_string_any": [],
            "trait_string_all": [],
            "trait_string_not": [],
            "min_rank": None,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 0.75,
            "token_id_any": [],
        },
        {
            "tier": 2,
            "trait_string_any": [],
            "trait_string_all": [],
            "trait_string_not": [],
            "min_rank": None,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 1.05,
            "token_id_any": [],
        },
    ],
    "bayc": [],
    "mayc": [],
    "cryptopunksv1": [
        {
            "tier": 1,
            "trait_string_any": ["""'trait_type': 'type', 'value': 'male'"""],
            "trait_string_all": [],
            "trait_string_not": [
                """'trait_type': 'accessory', 'value': 'stringy hair'"""
            ],
            "min_rank": None,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 0.9,
            "token_id_any": [],
        },
        {
            "tier": 2,
            "trait_string_any": ["""'trait_type': 'type', 'value': 'male'"""],
            "trait_string_all": [],
            "trait_string_not": [
                """'trait_type': 'accessory', 'value': 'stringy hair'"""
            ],
            "min_rank": None,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 1.05,
            "token_id_any": [],
        },
        {
            "tier": 1,
            "trait_string_any": [
                """'trait_type': 'accessory', 'value': 'cap forward'""",
                """'trait_type': 'accessory', 'value': 'nerd glasses'""",
                """'trait_type': 'accessory', 'value': 'crazy hair'""",
                """'trait_type': 'accessory', 'value': 'purple hair'""",
                """'trait_type': 'accessory', 'value': 'fedora'""",
                """'trait_type': 'accessory', 'value': 'cowboy hat'""",
                """'trait_type': 'accessory', 'value': 'police cap'""",
                """'trait_type': 'accessory', 'value': 'top hat'""",
                """'trait_type': 'accessory', 'value': '3d glasses'""",
                """'trait_type': 'accessory', 'value': 'vr'""",
                """'trait_type': 'accessory', 'value': 'hoodie'""",
            ],
            "trait_string_all": ["""'trait_type': 'type', 'value': 'male'"""],
            "trait_string_not": [
                """'trait_type': 'accessory', 'value': 'stringy hair'"""
            ],
            "min_rank": None,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 1.25,
            "token_id_any": [],
        },
        {
            "tier": 1,
            "trait_string_any": [],
            "trait_string_all": [],
            "trait_string_not": [],
            "min_rank": 150,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 1.5,
            "token_id_any": [],
        },
    ],
    "cryptoarte": [
        {
            "tier": 2,
            "trait_string_any": ["""'trait_type': 'Mint Year', 'value': '2018'"""],
            "trait_string_all": [],
            "trait_string_not": [],
            "min_rank": None,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": None,
            "token_id_any": [],
        },
        {
            "tier": 2,
            "trait_string_any": ["""'trait_type': 'Mint Year', 'value': '2020'"""],
            "trait_string_all": [],
            "trait_string_not": [],
            "min_rank": None,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": None,
            "token_id_any": [],
        },
        {
            "tier": 2,
            "trait_string_any": [
                """'trait_type': 'Mint Month', 'value': 'january'""",
                """'trait_type': 'Mint Month', 'value': 'february'""",
                """'trait_type': 'Mint Month', 'value': 'march'""",
            ],
            "trait_string_all": ["""'trait_type': 'Mint Year', 'value': '2019'"""],
            "trait_string_not": [],
            "min_rank": None,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": None,
            "token_id_any": [],
        },
        {
            "tier": 1,
            "trait_string_any": ["""'trait_type': 'Mint Year', 'value': '2018'"""],
            "trait_string_all": [],
            "trait_string_not": [],
            "min_rank": None,
            "max_abs_price": 1,
            "max_rel_flr_price_multiplier": None,
            "token_id_any": [],
        },
        {
            "tier": 1,
            "trait_string_any": ["""'trait_type': 'Mint Year', 'value': '2020'"""],
            "trait_string_all": [],
            "trait_string_not": [],
            "min_rank": None,
            "max_abs_price": 1,
            "max_rel_flr_price_multiplier": None,
            "token_id_any": [],
        },
        {
            "tier": 1,
            "trait_string_any": [
                """'trait_type': 'Mint Month', 'value': 'january'""",
                """'trait_type': 'Mint Month', 'value': 'february'""",
                """'trait_type': 'Mint Month', 'value': 'march'""",
            ],
            "trait_string_all": ["""'trait_type': 'Mint Year', 'value': '2019'"""],
            "trait_string_not": [],
            "min_rank": None,
            "max_abs_price": 0.55,
            "max_rel_flr_price_multiplier": None,
            "token_id_any": [],
        },
        {
            "tier": 1,
            "trait_string_any": [],
            "trait_string_all": [
                """'trait_type': 'Prime painting number', 'value': 'yes'""",
                """'trait_type': 'Golden miner on prime block', 'value': 'yes'""",
            ],
            "trait_string_not": [],
            "min_rank": None,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 1.2,
            "token_id_any": [],
        },
        {
            "tier": 2,
            "trait_string_any": [
                """'trait_type': 'Prime painting number', 'value': 'yes'""",
                """'trait_type': 'Golden miner on prime block', 'value': 'yes'""",
            ],
            "trait_string_all": [],
            "trait_string_not": [],
            "min_rank": None,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 1.15,
            "token_id_any": [],
        },
        {
            "tier": 2,
            "trait_string_any": [],
            "trait_string_all": [],
            "trait_string_not": [],
            "min_rank": None,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": None,
            "token_id_any": [i for i in range(0, 80)],
        },
        {
            "tier": 1,
            "trait_string_any": [],
            "trait_string_all": [],
            "trait_string_not": [],
            "min_rank": None,
            "max_abs_price": 2.5,
            "max_rel_flr_price_multiplier": None,
            "token_id_any": [i for i in range(0, 80)],
        },
    ],
    "cryptopunks": [],
    "pridepunks": [
        {
            "tier": 1,
            "trait_string_any": ["""'trait_type': 'type', 'value': 'male'"""],
            "trait_string_all": [],
            "trait_string_not": [
                """'trait_type': 'accessory', 'value': 'stringy hair'"""
            ],
            "min_rank": None,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 0.9,
            "token_id_any": [],
        },
        {
            "tier": 2,
            "trait_string_any": ["""'trait_type': 'type', 'value': 'male'"""],
            "trait_string_all": [],
            "trait_string_not": [
                """'trait_type': 'accessory', 'value': 'stringy hair'"""
            ],
            "min_rank": None,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 1.05,
            "token_id_any": [],
        },
        {
            "tier": 1,
            "trait_string_any": [
                """'trait_type': 'accessory', 'value': 'cap forward'""",
                """'trait_type': 'accessory', 'value': 'nerd glasses'""",
                """'trait_type': 'accessory', 'value': 'crazy hair'""",
                """'trait_type': 'accessory', 'value': 'purple hair'""",
                """'trait_type': 'accessory', 'value': 'fedora'""",
                """'trait_type': 'accessory', 'value': 'cowboy hat'""",
                """'trait_type': 'accessory', 'value': 'police cap'""",
                """'trait_type': 'accessory', 'value': 'top hat'""",
                """'trait_type': 'accessory', 'value': '3d glasses'""",
                """'trait_type': 'accessory', 'value': 'vr'""",
                """'trait_type': 'accessory', 'value': 'hoodie'""",
            ],
            "trait_string_all": ["""'trait_type': 'type', 'value': 'male'"""],
            "trait_string_not": [
                """'trait_type': 'accessory', 'value': 'stringy hair'"""
            ],
            "min_rank": None,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 1.25,
            "token_id_any": [],
        },
        {
            "tier": 1,
            "trait_string_any": [],
            "trait_string_all": [],
            "trait_string_not": [],
            "min_rank": 150,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 1.5,
            "token_id_any": [],
        },
    ],
    "cryptophunks": [
        {
            "tier": 1,
            "trait_string_any": ["""'trait_type': 'type', 'value': 'male'"""],
            "trait_string_all": [],
            "trait_string_not": [
                """'trait_type': 'accessory', 'value': 'stringy hair'"""
            ],
            "min_rank": None,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 0.9,
            "token_id_any": [],
        },
        {
            "tier": 2,
            "trait_string_any": ["""'trait_type': 'type', 'value': 'male'"""],
            "trait_string_all": [],
            "trait_string_not": [
                """'trait_type': 'accessory', 'value': 'stringy hair'"""
            ],
            "min_rank": None,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 1.05,
            "token_id_any": [],
        },
        {
            "tier": 1,
            "trait_string_any": [
                """'trait_type': 'accessory', 'value': 'cap forward'""",
                """'trait_type': 'accessory', 'value': 'nerd glasses'""",
                """'trait_type': 'accessory', 'value': 'crazy hair'""",
                """'trait_type': 'accessory', 'value': 'purple hair'""",
                """'trait_type': 'accessory', 'value': 'fedora'""",
                """'trait_type': 'accessory', 'value': 'cowboy hat'""",
                """'trait_type': 'accessory', 'value': 'police cap'""",
                """'trait_type': 'accessory', 'value': 'top hat'""",
                """'trait_type': 'accessory', 'value': '3d glasses'""",
                """'trait_type': 'accessory', 'value': 'vr'""",
                """'trait_type': 'accessory', 'value': 'hoodie'""",
            ],
            "trait_string_all": ["""'trait_type': 'type', 'value': 'male'"""],
            "trait_string_not": [
                """'trait_type': 'accessory', 'value': 'stringy hair'"""
            ],
            "min_rank": None,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 1.25,
            "token_id_any": [],
        },
        {
            "tier": 1,
            "trait_string_any": [],
            "trait_string_all": [],
            "trait_string_not": [],
            "min_rank": 150,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 1.5,
            "token_id_any": [],
        },
    ],
    "mooncats": [
        {
            "tier": 2,
            "trait_string_any": ["""'trait_type': 'Rescue Year', 'value': '2017'"""],
            "trait_string_all": [],
            "trait_string_not": [],
            "min_rank": None,
            "max_abs_price": 1.25,
            "max_rel_flr_price_multiplier": None,
            "token_id_any": [],
        },
        {
            "tier": 1,
            "trait_string_any": ["""'trait_type': 'Rescue Year', 'value': '2017'"""],
            "trait_string_all": [],
            "trait_string_not": [],
            "min_rank": None,
            "max_abs_price": 1,
            "max_rel_flr_price_multiplier": None,
            "token_id_any": [],
        },
    ],
    "nftworlds": [
        {
            "tier": 1,
            "trait_string_any": [],
            "trait_string_all": [],
            "trait_string_not": [],
            "min_rank": 1000,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 1.05,
            "token_id_any": [],
        },
        {
            "tier": 1,
            "trait_string_any": [],
            "trait_string_all": [],
            "trait_string_not": [],
            "min_rank": 500,
            "max_abs_price": None,
            "max_rel_flr_price_multiplier": 1.5,
            "token_id_any": [],
        },
    ],
}
