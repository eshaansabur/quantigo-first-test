import json
import itertools
import os
from collections import defaultdict

#read the file
filename='pos_0.png.json'
data_path = f'{filename}'
data = open(data_path)
#data= open(r`jsonfiles/filename`)
read_data=data.read()


#parse
parser = json.loads(read_data)
my_object = parser['objects']

#annotation objects
annotation_objects={

}
#annotation attributes
annotation_attributes={

}
#getting what type of objects in the array
object_Array=[]
for object in my_object:
    print(object['classTitle'])
    object_Array.append(object['classTitle'])

if 'Vehicle' in object_Array and 'License Plate' in object_Array:
    for element in my_object:
        # print(element['points'])
        my_points = element['points']
        exterior = my_points['exterior']
        b = []
        tags = element['tags']
        array = {}

        if element['classTitle'].lower() == 'vehicle':
            annotation_objects.update(
                {element['classTitle'].lower(): {"presence": 1, "bbox": list(itertools.chain(*exterior))}})
            for tag in tags:
                tagger = {tag['name']: tag['value']}
                array.update(tagger)
                annotation_attributes.update({element['classTitle'].lower(): array})
        elif element['classTitle'].lower() == 'license plate':
            annotation_objects.update(
                {element['classTitle'].lower(): {"presence": 1, "bbox": list(itertools.chain(*exterior))}})
            for tag in tags:
                tagger = {tag['name']: tag['value']}
                updated_array = array.update(tagger)
                array.update({"Occlusion": 0})
                annotation_attributes.update({element['classTitle'].lower(): array})
elif 'Vehicle' in object_Array:
    for element in my_object:
        # print(element['points'])
        my_points = element['points']
        exterior = my_points['exterior']
        b = []
        tags = element['tags']
        array = {}

        if element['classTitle'].lower() == 'vehicle':
            annotation_objects.update(
                {element['classTitle'].lower(): {"presence": 1, "bbox": list(itertools.chain(*exterior))}})
            for tag in tags:
                tagger = {tag['name']: tag['value']}
                array.update(tagger)
                annotation_attributes.update({element['classTitle'].lower(): array})
        #elif element['classTitle'].lower() == 'license plate':
                annotation_objects.update(
                {'license plate': {"presence": 0, "bbox": []}})
            for tag in tags:
                tagger = {tag['name']: tag['value']}
                updated_array = array.update(tagger)
                #array.update({"Occlusion": 0})
                annotation_attributes.update({element['classTitle'].lower(): array})
            annotation_attributes.update({"license_plate": {
                "Difficulty Score": None,
                "Value": None,
                "Occlusion": None
            }})
elif 'License Plate' in object_Array:
    for element in my_object:
        # print(element['points'])
        my_points = element['points']
        exterior = my_points['exterior']
        b = []
        tags = element['tags']
        array = {}

        if element['classTitle'].lower() == 'license plate':
            annotation_objects.update(
                {element['classTitle'].lower(): {"presence": 1, "bbox": list(itertools.chain(*exterior))}})
            for tag in tags:
                tagger = {tag['name']: tag['value']}
                array.update(tagger)
                annotation_attributes.update({element['classTitle'].lower(): array})
        #elif element['classTitle'].lower() == 'license plate':
                annotation_objects.update(
                {'vehicle': {"presence": 0, "bbox": []}})
            for tag in tags:
                tagger = {tag['name']: tag['value']}
                updated_array = array.update(tagger)
                array.update({"Occlusion": 0})
                annotation_attributes.update({element['classTitle'].lower(): array})
            annotation_attributes.update({"vehicle": {
                "Type": None,
                "Pose": None,
                "Model": None,
                "Make": None,
                "Color": None
            }})
else:
    annotation_objects.update(
        {"vehicle": {"presence": 0, "bbox": []}})
    annotation_objects.update(
        {"license plate": {"presence": 0, "bbox": []}})
    annotation_attributes.update({"vehicle": {
                "Type": None,
                "Pose": None,
                "Model": None,
                "Make": None,
                "Color": None
            }})
    annotation_attributes.update({"license_plate": {
                "Difficulty Score": None,
                "Value": None,
                "Occlusion": None
            }})

print(annotation_attributes)


#formatted object
formatted_object ={
    "dataset_name": filename,
    "image_link": "",
    "annotation_type": "image",
    "annotation_objects": annotation_objects,
"annotation_attributes": annotation_attributes
}

#dump into json frmat and file
list =[]
list.append(formatted_object)

formatted = 'formatted_'+filename
print(formatted)

with open(os.path.join("jsonfiles", formatted), "w") as output:
    json.dump(list, output)
