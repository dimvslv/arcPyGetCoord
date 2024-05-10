import arcpy
import pythonaddins

def get_unique_name(base_name):
    """Generate a unique layer name by appending numeric suffixes"""
    name = base_name
    count = 1
    while arcpy.Exists(name):
        name = "{}_{}".format(base_name, count)
        count += 1
    return name

def make_annotation_line(line, x, y):
    with arcpy.da.InsertCursor(name_line, ["SHAPE@", "longitude", "latitude"]) as line_cursor:
        line_cursor.insertRow([line, x, y])

mxd = arcpy.mapping.MapDocument("CURRENT")
layers = arcpy.mapping.ListLayers(mxd)

selected_layer = None

for layer in layers:
    if layer.getSelectionSet():
        selected_layer = layer
        break

if not selected_layer:
    pythonaddins.MessageBox("Select features to get coordinates", "Info", 0)

name_vertices = get_unique_name('vertices')
name_line = get_unique_name('line')
srid = arcpy.Describe(selected_layer).spatialReference

# if arcpy.Exists(r'in_memory\vertices'):
# arcpy.Delete_management(r'in_memory\vertices')

arcpy.CreateFeatureclass_management('in_memory', name_vertices, "POINT", spatial_reference=srid)
arcpy.AddField_management(name_vertices, "longitude", "DOUBLE")
arcpy.AddField_management(name_vertices, "latitude", "DOUBLE")

arcpy.CreateFeatureclass_management('in_memory', name_line, "POLYLINE", spatial_reference=srid)
arcpy.AddField_management(name_line, "longitude", "DOUBLE")
arcpy.AddField_management(name_line, "latitude", "DOUBLE")

edit = arcpy.da.Editor('in_memory')
edit.startEditing(False, True)
edit.startOperation()

with arcpy.da.InsertCursor(name_vertices, ["SHAPE@", "longitude", "latitude"]) as cursor:
    for row in arcpy.da.SearchCursor(selected_layer, ["SHAPE@"]):
        shape = row[0]
        if shape is not None:
            if shape.type == 'point' or shape.type == "multipoint":
                for point in shape:
                    if shape is not None:
                        x, y = point.X, point.Y
                        cursor.insertRow([point, x, y])
                        line = arcpy.Polyline(
                            arcpy.Array([arcpy.Point(x, y), arcpy.Point(x + 30, y + 30), arcpy.Point(x + 80, y + 30)]))
                        make_annotation_line(line, x, y)
            elif shape.type == "polygon" or shape.type == "multipolygon":
                for part in shape:
                    point_count = len(part)
                    for i, point in enumerate(part):
                        if point is not None:
                            if i == point_count - 1 and part[0].X == point.X and part[0].Y == point.Y:
                                continue
                            else:
                                x, y = point.X, point.Y
                                cursor.insertRow([point, x, y])
                                line = arcpy.Polyline(arcpy.Array(
                                    [arcpy.Point(x, y), arcpy.Point(x + 30, y + 30), arcpy.Point(x + 80, y + 30)]))
                                make_annotation_line(line, x, y)
            elif shape.type == "polyline" or shape.type == "multilinestring":
                for part in shape:
                    for point in part:
                        if point is not None:
                            x, y = point.X, point.Y
                            cursor.insertRow([point, x, y])
                            line = arcpy.Polyline(arcpy.Array([arcpy.Point(x, y), arcpy.Point(x + 30, y + 30), arcpy.Point(x + 80, y + 30)]))
                            make_annotation_line(line, x, y)

edit.stopEditing(True)
del mxd

# show labels
lyr = arcpy.mapping.Layer(name_line)
lyr.showLabels = True
lyr.labelClasses[0].expression = '"X: " & [longitude] & " " & vbCrLf & "Y: " & [latitude]'
arcpy.RefreshActiveView()

# create annotation polyline
'''
line = arcpy.Polyline(arcpy.Array([arcpy.Point(0, 0), arcpy.Point(1, 1), arcpy.Point(2, 2)]))
arcpy.CreateFeatureclass_management('in_memory', 'line', "POLYLINE")
with arcpy.da.InsertCursor('line', ["SHAPE@"]) as cursor:
    cursor.insertRow([line])
    '''