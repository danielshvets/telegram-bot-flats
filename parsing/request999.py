import requests
import json
import fake_useragent
import copy

user = fake_useragent.UserAgent().random
LINK = 'https://999.md/graphql'

DRY_REQ = {
	"operationName": "SearchAds",
	"query": "query SearchAds($input: Ads_SearchInput!, $isWorkCategory: Boolean = false, $includeCarsFeatures: Boolean = false, $includeBody: Boolean = false, $includeOwner: Boolean = false, $includeBoost: Boolean = false, $locale: Common_Locale) {\n  searchAds(input: $input) {\n    ads {\n      ...AdsSearchFragment\n      __typename\n    }\n    count\n    reseted\n    __typename\n  }\n}\n\nfragment AdsSearchFragment on Advert {\n  ...AdListFragment\n  ...WorkCategoryFeatures @include(if: $isWorkCategory)\n  reseted(\n    input: {format: \"2 Jan. 2006, 15:04\", locale: $locale, timezone: \"Europe/Chisinau\", getDiff: false}\n  )\n  __typename\n}\n\nfragment AdListFragment on Advert {\n  id\n  title\n  subCategory {\n    ...CategoryAdFragment\n    __typename\n  }\n  ...PriceAndImages\n  ...CarsFeatures @include(if: $includeCarsFeatures)\n  ...AdvertOwner @include(if: $includeOwner)\n  transportYear: feature(id: 19) {\n    ...FeatureValueFragment\n    __typename\n  }\n  author: feature(id: 795) {\n    ...FeatureValueFragment\n    __typename\n  }\n  body: feature(id: 13) @include(if: $includeBody) {\n    ...FeatureValueFragment\n    __typename\n  }\n  uploadedVideos: feature(id: 2562) {\n    ...FeatureValueFragment\n    __typename\n  }\n  ...AdvertBooster @include(if: $includeBoost)\n  label: displayProduct(alias: LABEL) {\n    ... on DisplayLabel {\n      enable\n      ...DisplayLabelFragment\n      __typename\n    }\n    __typename\n  }\n  frame: displayProduct(alias: FRAME) {\n    ... on DisplayFrame {\n      enable\n      __typename\n    }\n    __typename\n  }\n  animation: displayProduct(alias: ANIMATION) {\n    ... on DisplayAnimation {\n      enable\n      __typename\n    }\n    __typename\n  }\n  animationAndFrame: displayProduct(alias: ANIMATION_AND_FRAME) {\n    ... on DisplayAnimationAndFrame {\n      enable\n      __typename\n    }\n    __typename\n  }\n  condition: feature(id: 593) {\n    ...FeatureValueFragment\n    __typename\n  }\n  owner {\n    business {\n      plan\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment CategoryAdFragment on Category {\n  id\n  title {\n    ...TranslationFragment\n    __typename\n  }\n  parent {\n    id\n    title {\n      ...TranslationFragment\n      __typename\n    }\n    parent {\n      id\n      title {\n        ...TranslationFragment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment TranslationFragment on I18NTr {\n  translated\n  __typename\n}\n\nfragment PriceAndImages on Advert {\n  price: feature(id: 2) {\n    ...FeatureValueFragment\n    __typename\n  }\n  pricePerMeter: feature(id: 1385) {\n    ...FeatureValueFragment\n    __typename\n  }\n  oldPrice: feature(id: 1640) {\n    ...FeatureValueFragment\n    __typename\n  }\n  images: feature(id: 14) {\n    ...FeatureValueFragment\n    __typename\n  }\n  __typename\n}\n\nfragment FeatureValueFragment on FeatureValue {\n  id\n  type\n  value\n  __typename\n}\n\nfragment CarsFeatures on Advert {\n  carFuel: feature(id: 151) {\n    ...FeatureValueFragment\n    __typename\n  }\n  carDrive: feature(id: 108) {\n    ...FeatureValueFragment\n    __typename\n  }\n  carTransmission: feature(id: 101) {\n    ...FeatureValueFragment\n    __typename\n  }\n  mileage: feature(id: 104) {\n    ...FeatureValueFragment\n    __typename\n  }\n  engineVolume: feature(id: 103) {\n    ...FeatureValueFragment\n    __typename\n  }\n  __typename\n}\n\nfragment AdvertOwner on Advert {\n  owner {\n    ...AccountFragment\n    __typename\n  }\n  __typename\n}\n\nfragment AccountFragment on Account {\n  id\n  login\n  avatar\n  createdDate\n  business {\n    plan\n    id\n    __typename\n  }\n  verification {\n    isVerified\n    date(input: {timezone: \"Europe/Chisinau\", getDiff: false})\n    __typename\n  }\n  __typename\n}\n\nfragment AdvertBooster on Advert {\n  booster: product(alias: BOOSTER_V2) {\n    enable\n    __typename\n  }\n  __typename\n}\n\nfragment DisplayLabelFragment on DisplayLabel {\n  title\n  color {\n    ...ColorFragment\n    __typename\n  }\n  gradient {\n    ...GradientFragment\n    __typename\n  }\n  __typename\n}\n\nfragment ColorFragment on Common_Color {\n  r\n  g\n  b\n  a\n  __typename\n}\n\nfragment GradientFragment on Gradient {\n  from {\n    ...ColorFragment\n    __typename\n  }\n  to {\n    ...ColorFragment\n    __typename\n  }\n  position\n  rotation\n  __typename\n}\n\nfragment WorkCategoryFeatures on Advert {\n  salary: feature(id: 266) {\n    ...FeatureValueFragment\n    __typename\n  }\n  workSchedule: feature(id: 260) {\n    ...FeatureValueFragment\n    __typename\n  }\n  workExperience: feature(id: 263) {\n    ...FeatureValueFragment\n    __typename\n  }\n  education: feature(id: 261) {\n    ...FeatureValueFragment\n    __typename\n  }\n  __typename\n}",
	"variables": {
		"includeBody": False,
		"includeBoost": False,
		"includeCarsFeatures": False,
		"includeOwner": False,
		"input": {
			"filters": [
			],
			"pagination": {
				"limit": None,
				"skip": 0
			},
			"sort": "SORT_ADS_DATE_DESC",
			"source": "AD_SOURCE_DESKTOP_REDESIGN",
			"subCategoryId": 1404
		},
		"isWorkCategory": False,
		"locale": "ru_RU"
	}
}


FILTERS = {
    "offer_type": {
        "filterId": 16,
        "featureId": 1,
        "options": {
            "sell": 776,
            "rent": 912
        }
    },
    "rooms_amount": {
        "filterId": 30,
        "featureId": 241,
        "options": {
            "aroom": 908,
            "one_room_flat": 893,
            "two_rooms_flat": 894,
            "three_rooms_flat": 902 
        }
    },
    "housing_stock": {
        "filterId": 2307,
        "featureId": 852,
        "options": {
            "secondary": 19109,
            "new": 19108
        }
    }
}

def get_response(user_data: dict):
    payload = copy.deepcopy(DRY_REQ)

    for key, values in user_data.items():
        if key not in FILTERS:  # ← пропускаем лишние ключи
            continue
        if not values:  # ← пропускаем пустые списки
            continue

        payload["variables"]["input"]["filters"].append({
            "filterId": FILTERS[key]["filterId"],
            "features": [{
                "featureId": FILTERS[key]["featureId"],
                "optionIds": [
                    FILTERS[key]["options"][v]
                    for v in values
                ]
            }]
        })

    return requests.post(LINK, json=payload).json()
    




print(type(DRY_REQ["variables"]["input"]["filters"]))
