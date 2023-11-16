import json

import fiona

from tqdm import tqdm
from shapely.geometry import shape

geojson_file = 'RockyMountainNationalParkTrails.geojson'

# Small dataset, doing this for efficiency, unable to loop through the features again once started with fiona 
# (n^2) Could use grass, gdal, or sqlite but do not have either on my personal computer
data = fiona.open(geojson_file)
data_1 = fiona.open(geojson_file)


data_overlay = {}
for feature in tqdm(data, desc='Looping through Geometries'):

    # Create a shape object
    feature_shape = shape(feature['geometry'])

    # A list to append IDs
    features_intersect = []

    # Loop though and see if any objects intersect
    for compare_feature in data_1:
        
        # If same object skip
        if compare_feature['id'] == feature['id']:
            continue

        # Create a shape object for compare
        compare_shape = shape(compare_feature['geometry'])
        
        # If they intersect, append the ID
        if feature_shape.intersects(compare_shape):
            if feature_shape.intersection(compare_shape).area == 0.0:
                continue
            features_intersect.append(compare_feature['id'])

    # If there is a list append it to the dictionary
    if len(features_intersect) > 0:
        print(feature['id'])
        data_overlay[feature['id']] = features_intersect

with open('intersects.json', 'w') as f:
    f.write(json.dumps(data_overlay))