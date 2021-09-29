import os
import cv2
from xml.dom.minidom import Document

# windows下无需
import sys

stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
#reload(sys)
#sys.setdefaultencoding('utf-8')
sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde

# category_set = ['car', 'sea', 'airplane']


def custombasename(fullname):
    return os.path.basename(os.path.splitext(fullname)[0])


def limit_value(a, b):
    if a < 1:
        a = 1
    if a >= b:
        a = b - 1
    return a


def readlabeltxt(txtpath, height, width, hbb=False):
    print(txtpath)
    with open(txtpath, 'r') as f_in:  # 打开txt文件
        lines = f_in.readlines()
        splitlines = [x.strip().split(' ') for x in lines]  # 根据空格分割
        boxes = []
        for i, splitline in enumerate(splitlines):
            if i in [0, 1]:  # DOTA数据集前两行对于我们来说是无用的
                imageSource = (str(splitlines[0][0])).split(':')[1]
                resolution = (str(splitlines[1][0])).split(':')[1]
                continue
            label = splitline[8]
            dif=splitline[9]
            # if label not in category_set:  # 只书写制定的类别
            #     continue
            x1 = int(float(splitline[0])+0.5)
            y1 = int(float(splitline[1])+0.5)
            x2 = int(float(splitline[2])+0.5)
            y2 = int(float(splitline[3])+0.5)
            x3 = int(float(splitline[4])+0.5)
            y3 = int(float(splitline[5])+0.5)
            x4 = int(float(splitline[6])+0.5)
            y4 = int(float(splitline[7])+0.5)
            # 如果是hbb
            if hbb:
                xx1 = min(x1, x2, x3, x4)
                xx2 = max(x1, x2, x3, x4)
                yy1 = min(y1, y2, y3, y4)
                yy2 = max(y1, y2, y3, y4)

                xx1 = limit_value(xx1, width)
                xx2 = limit_value(xx2, width)
                yy1 = limit_value(yy1, height)
                yy2 = limit_value(yy2, height)

                box = [xx1, yy1, xx2, yy2, label,dif]
                boxes.append(box)
            else:  # 否则是obb
                x1 = limit_value(x1, width)
                y1 = limit_value(y1, height)
                x2 = limit_value(x2, width)
                y2 = limit_value(y2, height)
                x3 = limit_value(x3, width)
                y3 = limit_value(y3, height)
                x4 = limit_value(x4, width)
                y4 = limit_value(y4, height)

                box = [x1, y1, x2, y2, x3, y3, x4, y4, label,dif]
                boxes.append(box)
    return boxes,imageSource,resolution


def writeXml(tmp, imgname, w, h, d, bboxes, hbb=True,pic_path = "null",img_source="null",img_resolution="null",json_path = "null"):
    doc = Document()
    # owner
    AISample = doc.createElement('AISample')
    doc.appendChild(AISample)
    # AIMetadata
    AIMetadata = doc.createElement('AIMetadata')
    AISample.appendChild(AIMetadata)

    #identification
    Identification = doc.createElement('Identification')
    AIMetadata.appendChild(Identification)

    DocumentTitle = doc.createElement('DocumentTitle')
    Identification.appendChild(DocumentTitle)
    DocumentTxt = doc.createTextNode("VOC2007")
    DocumentTitle.appendChild(DocumentTxt)

    Version = doc.createElement('Version')
    Identification.appendChild(Version)
    VersionTxt = doc.createTextNode("1.5")
    Version.appendChild(VersionTxt)

    Purpose = doc.createElement('Purpose')
    Identification.appendChild(Purpose)
    PurposeTxt = doc.createTextNode("Object Detection")
    Purpose.appendChild(PurposeTxt)

    Abstract = doc.createElement('Abstract')
    Identification.appendChild(Abstract)
    AbstractTxt = doc.createTextNode("DOTA-v1.5 contains 400,000 annotated object instances in 16 categories. This is an updated version of DOTA-v1.0. They all use the same aerial images, but DOTA-v1.5 modified and updated the objects Many of the small object instances below 10 pixels that were missing in DOTA-v1.0 have been additionally annotated, and the category of DOTA-v1.5 has also been expanded")
    Abstract.appendChild(AbstractTxt)

    SampleCreator = doc.createElement('SampleCreator')
    Identification.appendChild(SampleCreator)
    SampleCreatorTxt = doc.createTextNode("Panyinyin")
    SampleCreator.appendChild(SampleCreatorTxt)

    SampleDate = doc.createElement('SampleDate')
    Identification.appendChild(SampleDate)
    SampleDateTxt = doc.createTextNode("20190000")
    SampleDate.appendChild(SampleDateTxt)

    SampleSize = doc.createElement('SampleSize')
    Identification.appendChild(SampleSize)
    SampleSizeTxt = doc.createTextNode("400000")
    SampleSize.appendChild(SampleSizeTxt)

    SampleLabeler = doc.createElement('SampleLabeler')
    Identification.appendChild(SampleLabeler)
    SampleLabelerTxt = doc.createTextNode("Unspecified")
    SampleLabeler.appendChild(SampleLabelerTxt)

    # LabelDate = doc.createElement('LabelDate')
    # Identification.appendChild(LabelDate)
    # LabelDateTxt = doc.createTextNode("Unspecified")
    # LabelDate.appendChild(LabelDateTxt)

    # SpatialRepresentation
    SpatialRepresentation = doc.createElement('SpatialRepresentation')
    AIMetadata.appendChild(SpatialRepresentation)

    GeometricObjects = doc.createElement('GeometricObjects')
    SpatialRepresentation.appendChild(GeometricObjects)
    GeometricObjectsTxt = doc.createTextNode("polygon")
    GeometricObjects.appendChild(GeometricObjectsTxt)

    Topology = doc.createElement('Topology')
    SpatialRepresentation.appendChild(Topology)
    TopologyTxt = doc.createTextNode("Unspecified")
    Topology.appendChild(TopologyTxt)

    Extent = doc.createElement('Extent')
    SpatialRepresentation.appendChild(Extent)
    ExtentTxt = doc.createTextNode("Unspecified")
    Extent.appendChild(ExtentTxt)

    # CoordinateReferenceSystem
    CoordinateReferenceSystem = doc.createElement('CoordinateReferenceSystem')
    AIMetadata.appendChild(CoordinateReferenceSystem)

    # CoordinateReferenceSystem
    Constraints = doc.createElement('Constraints')
    AIMetadata.appendChild(Constraints)

    AccessConstraints = doc.createElement('AccessConstraints')
    Constraints.appendChild(AccessConstraints)
    AccessConstraintsTxt = doc.createTextNode("Unspecified")
    AccessConstraints.appendChild(AccessConstraintsTxt)

    Uselimitations = doc.createElement('Uselimitations')
    Constraints.appendChild(Uselimitations)
    UselimitationsTxt = doc.createTextNode("Unspecified")
    Uselimitations.appendChild(UselimitationsTxt)

    # DataQuality
    DataQuality = doc.createElement('DataQuality')
    AIMetadata.appendChild(DataQuality)

    # Completeness
    Completeness = doc.createElement('Completeness')
    DataQuality.appendChild(Completeness)

    excessItem = doc.createElement('excessItem')
    Completeness.appendChild(excessItem)
    excessItemTxt = doc.createTextNode("Unspecified")
    excessItem.appendChild(excessItemTxt)

    excessItemRate = doc.createElement('excessItemRate')
    Completeness.appendChild(excessItemRate)
    excessItemRateTxt = doc.createTextNode("Unspecified")
    excessItemRate.appendChild(excessItemRateTxt)

    excessItemNum = doc.createElement('excessItemNum')
    Completeness.appendChild(excessItemNum)
    excessItemNumTxt = doc.createTextNode("Unspecified")
    excessItemNum.appendChild(excessItemNumTxt)

    duplicateItemNum = doc.createElement('duplicateItemNum')
    Completeness.appendChild(duplicateItemNum)
    duplicateItemNumTxt = doc.createTextNode("Unspecified")
    duplicateItemNum.appendChild(duplicateItemNumTxt)

    # CompletenessTxt = doc.createTextNode("Unspecified")
    # Completeness.appendChild(CompletenessTxt)

    # LogicalConsistency
    LogicalConsistency = doc.createElement('LogicalConsistency')
    DataQuality.appendChild(LogicalConsistency)

    FormatConsistency= doc.createElement('FormatConsistency')
    LogicalConsistency.appendChild(FormatConsistency)
    FormatConsistencyTxt = doc.createTextNode("Unspecified")
    FormatConsistency.appendChild(FormatConsistencyTxt)

    DomainConsistency = doc.createElement('DomainConsistency')
    LogicalConsistency.appendChild(DomainConsistency)
    DomainConsistencyTxt = doc.createTextNode("Unspecified")
    DomainConsistency.appendChild(DomainConsistencyTxt)

    # LogicalConsistencyTxt = doc.createTextNode("Unspecified")
    # LogicalConsistency.appendChild(LogicalConsistencyTxt)

    # ThematicAccuracy
    ThematicAccuracy = doc.createElement('ThematicAccuracy')
    DataQuality.appendChild(ThematicAccuracy)
    # ThematicAccuracyTxt = doc.createTextNode("Unspecified")
    # ThematicAccuracy.appendChild(ThematicAccuracyTxt)
    ClassificationCorrectness = doc.createElement('ClassificationCorrectness')
    ThematicAccuracy.appendChild(ClassificationCorrectness)
    ClassificationCorrectnessTxt = doc.createTextNode("Unspecified")
    ClassificationCorrectness.appendChild(ClassificationCorrectnessTxt)


    # PositionalAccuracy
    PositionalAccuracy = doc.createElement('PositionalAccuracy')
    DataQuality.appendChild( PositionalAccuracy)
    # PositionalAccuracyTxt = doc.createTextNode("Unspecified")
    # PositionalAccuracy.appendChild( PositionalAccuracyTxt)
    PositionBias = doc.createElement('PositionBias')
    PositionalAccuracy.appendChild(PositionBias)
    PositionBiasTxt = doc.createTextNode("Unspecified")
    PositionBias.appendChild(PositionBiasTxt)

    UncertaintiesMean = doc.createElement('UncertaintiesMean')
    PositionalAccuracy.appendChild(UncertaintiesMean)
    UncertaintiesMeanTxt = doc.createTextNode("Unspecified")
    UncertaintiesMean.appendChild(UncertaintiesMeanTxt)


    # Usability
    Usability = doc.createElement('Usability')
    DataQuality.appendChild(Usability)
    UsabilityTxt = doc.createTextNode("Unspecified")
    Usability.appendChild(UsabilityTxt)

    # ClassBalance
    ClassBalance = doc.createElement('ClassBalance')
    DataQuality.appendChild(ClassBalance)
    ClassBalanceTxt = doc.createTextNode("Unspecified")
    ClassBalance.appendChild(ClassBalanceTxt)

    # Provenance
    Provenance = doc.createElement('Provenance')
    AIMetadata.appendChild(Provenance)

    SampleLabeler = doc.createElement('SampleLabeler')
    Provenance.appendChild(SampleLabeler)
    SampleLabelerTxt = doc.createTextNode("Unspecified")
    SampleLabeler.appendChild(SampleLabelerTxt)

    LabelDate = doc.createElement('LabelDate')
    Provenance.appendChild(LabelDate)
    LabelDateTxt = doc.createTextNode("Unspecified")
    LabelDate.appendChild(LabelDateTxt)

    Modifier = doc.createElement('Modifier')
    Provenance.appendChild(Modifier)
    ModifierTxt = doc.createTextNode("Unspecified")
    Modifier.appendChild(ModifierTxt)

    ModifyDate = doc.createElement('ModifyDate')
    Provenance.appendChild(ModifyDate)
    ModifyDateTxt = doc.createTextNode("Unspecified")
    ModifyDate.appendChild(ModifyDateTxt)

    ModifyContext = doc.createElement('ModifyContext')
    Provenance.appendChild(ModifyContext)
    ModifyContextTxt = doc.createTextNode("Unspecified")
    ModifyContext.appendChild(ModifyContextTxt)

    ProcessStep = doc.createElement('ProcessStep')
    Provenance.appendChild(ProcessStep)
    ProcessStepTxt = doc.createTextNode("Unspecified")
    ProcessStep.appendChild(ProcessStepTxt)

    # SampleJson Link
    SampleLink = doc.createElement('SampleLink')
    AIMetadata.appendChild(SampleLink)

    SampleLabeler = doc.createElement('SampleLabeler')
    Provenance.appendChild(SampleLabeler)
    SampleLabelerTxt = doc.createTextNode("Unspecified")
    SampleLabeler.appendChild(SampleLabelerTxt)

    SampleJson =doc.createElement('SampleJson')
    SampleLink.appendChild(SampleJson)
    SampleJsonTxt = doc.createTextNode(json_path)
    SampleJson.appendChild(SampleJsonTxt)


    xmlname = os.path.splitext(imgname)[0]
    tempfile = os.path.join(tmp, xmlname +'_metadata'+'.xml')
    with open(tempfile, 'wb') as f:
        f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))
    return



if __name__ == '__main__':
    # data_path = '/home/yantianwang/lala/ship/train/examplesplit'
    # data_path = 'I:\object detection\3_4DOTA\train'
    data_path = r'D:\SampleML\sampleMLV2'
    images_path = os.path.join(data_path, 'image')  # 样本图片路径
    imageName = os.listdir(images_path)
    labeltxt_path = os.path.join(data_path, 'label')  # DOTA标签的所在路径
    json_path = os.path.join(data_path,'json')
    anno_new_path = os.path.join(data_path, 'xml')  # 新的voc格式存储位置（hbb形式）
    ext = '.png'  # 样本图片的后缀
    filenames = os.listdir(labeltxt_path)  # 获取每一个txt的名称
    filenames.sort()
    jsonfileName = os.listdir(json_path)
    jsonfileName.sort()
    for i in range(len(filenames)):
        filepath = labeltxt_path + '/' + filenames[i]  # 每一个DOTA标签的具体路径
        jsonpath = json_path + '/' + jsonfileName[i]
        picname = os.path.splitext(filenames[i])[0] + ext
        pic_path = os.path.join(images_path, picname)
        im = cv2.imread(pic_path)  # 读取相应的图片
        (H, W, D) = im.shape  # 返回样本的大小
        boxes,img_source,img_resolution = readlabeltxt(filepath, H, W, hbb=True)  # 默认是矩形（hbb）得到gt  fnn代表
        if len(boxes) == 0:
            print('文件为空', filepath)
        # 读取对应的样本图片，得到H,W,D用于书写xml
        # 书写xml
        writeXml(anno_new_path, picname, W, H, D, boxes, hbb=True,pic_path = pic_path,img_source = img_source,img_resolution = img_resolution,json_path = jsonpath)
        print('正在处理%s' % filenames[i])
#
# import cv2
# pic_path = 'D:\\tianzhibei\\testimset\\images\\16-11.jpg'
# im = cv2.imread(pic_path)  # 读取相应的图片
# (H, W, D) = im.shape  # 返回样本的大小