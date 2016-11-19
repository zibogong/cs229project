import os.path
import xml.etree.ElementTree as ET
import shutil
import Image
'''
hello
please comment
'''
def addobject(newroot, name, xmin, ymin, xmax, ymax):
    newobj = ET.SubElement(newroot, 'object')
    newname = ET.SubElement(newobj, 'name')
    newname.text = name
    newpose = ET.SubElement(newobj, 'pose')
    newpose.text = 'Unspecified'
    newtruncated = ET.SubElement(newobj, 'truncated')
    newtruncated.text = '0'
    newdiff = ET.SubElement(newobj, 'difficult')
    newdiff.text = '0'
    newbnbbox = ET.SubElement(newobj, 'bnbbox')
    newxmin = ET.SubElement(newbnbbox, 'xmin')
    newxmin.text = str(xmin)
    newymin = ET.SubElement(newbnbbox, 'ymin')
    newymin.text = str(ymin)
    newxmax =f ET.SubElement(newbnbbox, 'xmax')
    newxmax.text = str(xmax)
    newymax = ET.SubElement(newbnbbox, 'ymax')
    newymax.text = str(ymax)

def generate_xml(xml_path, i, xml_output_path, image_input_path, image_output_path):
    newroot = ET.Element('annotation')
    print xml_path
    tree = ET.parse(xml_path)
    root = tree.getroot()
    filename = root.find('filename').text.strip()
    folder = root.find('folder').text.strip()
    image_path = image_input_path + folder + '/' + filename
    image = Image.open(image_path)
    ncol = image.size[0]
    nrow = image.size[1]
    #nrow = root.find('imagesize').find('nrows').text.strip()
    #ncol = root.find('imagesize').find('ncols').text.strip()
    newfolder = ET.SubElement(newroot, 'folder')
    newfolder.text = 'VOC2007'
    newfilename = ET.SubElement(newroot, 'filename')
    newfilename.text = str(i).zfill(6) + '.jpg'
    newsize = ET.SubElement(newroot, 'size')
    newwidth = ET.SubElement(newsize, 'width')
    newwidth.text = str(ncol)
    newheight = ET.SubElement(newsize, 'height')
    newheight.text = str(nrow)
    newdepth = ET.SubElement(newsize, 'depth')
    newdepth.text = str(3)
    newfilename.text = str(i).zfill(6) + '.jpg'
    x = 0
    for child in root:
        if child.tag == 'object':
            name = child.find('name').text.strip()
            if not name in ['table lamp', 'bottle', 'towel', 'backpack']:
                continue
            poly = child.find('polygon')
            xmin = 9999
            xmax = -9999
            ymin = 9999
            ymax = -9999
            for pt in poly:
                if pt.tag == 'pt':
                    x = int(pt.find('x').text)
                    y = int(pt.find('y').text)
                    if(x < xmin):
                        xmin = x
                    if(x > xmax):
                        xmax = x
                    if(y < ymin):
                        ymin = y
                    if(y > ymax):
                        ymax = y
            addobject(newroot, name, xmin, ymin, xmax, ymax)
            x = x + 1
    nofuckplease = ET.ElementTree(newroot)
    if x > 0:
        nofuckplease.write(xml_output_path + str(i).zfill(6) + '.xml')
        shutil.copy(image_path, image_output_path + str(i).zfill(6) + '.jpg')
        return True
    return False

xmls_path = "/data/SUN2012/Annotations/"
xml_output_path = "/data/Annotations/"
image_output_path = "/data/Images/"
image_input_paht = "/data/SUN2012/Images/"
i = 0
for parent,dirnames,filenames in os.walk(xmls_path):
    for filename in filenames:
        if '.xml' in filename:
            if generate_xml(parent + '/' + filename, i, xml_output_path, image_input_paht, image_output_path):
                i = i + 1
