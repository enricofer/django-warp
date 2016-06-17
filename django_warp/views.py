from django.shortcuts import render
from django.conf import settings
from .models import rasterMaps, datasets
from .forms import UploadImmagineSorgenteForm, DatasetForm
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.contrib.gis.gdal import GDALRaster
from django.contrib.auth.decorators import login_required, user_passes_test
from random import randint
from slugify import slugify
import json
import sys
import os

# lib

def handle_uploaded_file(f,pk):
    fileRelativeToMediaRoot = 'warp/%s_s_%s' % ('0000'[:4-len(str(pk))]+str(pk),f.name)
    fileAbsolutePath = settings.MEDIA_ROOT + fileRelativeToMediaRoot
    try:
        os.makedirs(os.path.dirname(fileAbsolutePath))
    except FileExistsError: 
        pass
    with open(fileAbsolutePath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return fileRelativeToMediaRoot

def removableDSList():
    removable = []
    for d in datasets.objects.all():
        georefs = rasterMaps.objects.filter(dataset=d)
        if not georefs:
            removable.append(d.pk)
    return removable

# Create your views here.


def dataset_list (request,datasetId):
    dataset_items = rasterMaps.objects.all().order_by('pk')
    dataset_obj = datasets.objects.get(pk=datasetId)
    
    #reorder datasets to have TRASH as last item
    datasets_list = datasets.objects.all().order_by('pk')
    datasets_items = []
    trash_item = None
    for dataset in datasets_list:
        if dataset.name != "__TRASH":
            datasets_items.append(dataset)
        else:
            trash_item = dataset
    if trash_item:
        datasets_items.append(trash_item)
    return render(request, 'collapse_list.html', {'items': dataset_items, 'groups': datasets_items, 'settings': settings, 'choice': int(datasetId)})

@login_required(login_url='/warp/login/')
@user_passes_test(lambda u: u.is_staff)
def datasets_list (request, alert=None):
    datasets_list = datasets.objects.all().order_by('pk')
    datasets_items = []
    trash_item = None
    for dataset in datasets_list:
        if dataset.name != "__TRASH":
            datasets_items.append(dataset)
        else:
            trash_item = dataset
    if trash_item:
        datasets_items.append(trash_item)
    return render(request, 'datasets_list.html', {'items': datasets_items, 'alert': alert, 'removable':removableDSList()})

@login_required(login_url='/warp/login/')
@user_passes_test(lambda u: u.is_staff)
def remove_dataset (request, dataset):
    dataset_obj = datasets.objects.get(pk=dataset)
    dataset_name = dataset_obj.name
    #test if void or not
    georefs = rasterMaps.objects.filter(dataset=dataset_obj)
        
    if dataset_name == "__TRASH":
        empty_trash()
        message = "TRASH empty"
        className = "alert-success"
    else:
        if georefs:
            message = "Can't remove not empty Dataset %s" % dataset_name
            className = "alert-warning"
            
        else:
            message = "Dataset %s successfully removed" % dataset_name
            className = "alert-success"
            dataset_obj.delete()
    response = datasets_list (request, alert={'class':className, 'message': message })
    return response

@login_required(login_url='/warp/login/')
@user_passes_test(lambda u: u.is_superuser)
def empty_trash(request):
    trash_dataset = get_trash_dataset() 
    trashed_images = rasterMaps.objects.filter(dataset = trash_dataset)
    for image in trashed_images:
        image.delete()
    return HttpResponseRedirect('/warp/')

@login_required(login_url='/warp/login/')
@user_passes_test(lambda u: u.is_staff)
def dataset_form (request, datasetId = None):
    if request.method == 'POST':
        form = DatasetForm(request.POST)
        if form.is_valid():
            if datasetId:
                datasetItem = datasets.objects.get(pk=datasetId)
            else:
                datasetItem = datasets()

            try:
                referenced = rasterMaps.objects.get(dataset=datasetId)
            except:
                referenced = None

            if not referenced:
                datasetItem.epsg = form.data['epsg']
                
            if str(datasetItem.epsg) == str(form.data['epsg']):
                
                print ("extent",form.data['extentLeft'], file=sys.stderr)
                datasetItem.baselayer = form.data['baselayer']
                datasetItem.extentLeft = form.data['extentLeft']
                datasetItem.extentBottom = form.data['extentBottom']
                datasetItem.extentRight = form.data['extentRight']
                datasetItem.extentTop = form.data['extentTop']

            datasetItem.name = form.data['name']
            datasetItem.slug = slugify (form.data['name'])
            datasetItem.save()
            print ("UPDATE",request.POST.get('update', ''), file=sys.stderr)
            if request.POST.get('update', '') == '1':
                return HttpResponseRedirect('/warp/editdataset/'+str(datasetId)+'/')
            else:
                return HttpResponseRedirect('/warp/')
        else:
            return render(request, 'dataset_form.html', {'idx': datasetId, 'form': form})
                
    if datasetId:
        editDataset = datasets.objects.get(pk=datasetId)
        form = DatasetForm(instance = editDataset)
    else:
        form = DatasetForm()
    
    return render(request, 'dataset_form.html', {'idx': datasetId, 'form': form})

def get_trash_dataset():
    try:
        trash_dataset = datasets.objects.get(name="__TRASH")
    except:
        trash_dataset = None
    return trash_dataset

def dataset_view (request, datasetId = None):
    dataset = datasets.objects.get(pk=datasetId)
    dataset_imgs = rasterMaps.objects.filter(dataset=datasetId)
    map_images = []
    for map_image in dataset_imgs:
        if map_image.webimg:
            raster = GDALRaster(settings.MEDIA_ROOT + str(map_image.webimg), write=False)
            map_images.append({
                'titolo': map_image.titolo,
                'url':settings.MEDIA_URL + str(map_image.webimg)+"?dum="+str(randint(1000000,9999999)),
                'size':[map_image.webimg.width,map_image.webimg.height],
                'extent':[raster.extent[0],raster.extent[1],raster.extent[2],raster.extent[3]]
            })
    return render(request, 'dataset_view.html', {'idx': datasetId, 'images': map_images, 'dataset':dataset, 'settings':settings})
    

@login_required(login_url='/warp/login/')
def trash_image(request, idx = None):
    trash_dataset = get_trash_dataset()
    if not trash_dataset:
        trash_dataset = datasets()
        trash_dataset.name = "__TRASH"
        trash_dataset.slug = "__TRASH"
        trash_dataset.epsg = 0
        trash_dataset.extentLeft = 0
        trash_dataset.extentBottom = 0
        trash_dataset.extentRight = 0
        trash_dataset.extentTop = 0
        trash_dataset.save()
    trash_item = rasterMaps.objects.get(pk=idx)
    if not trash_item.datasetRecover:
        trash_item.datasetRecover = trash_item.dataset
        oldDataset = trash_item.dataset.pk
        trash_item.dataset = trash_dataset
        trash_item.save()
    response = dataset_list(request, oldDataset)
    return response


@login_required(login_url='/warp/login/')
def recover_image(request, idx = None):
    try:
        recover_image = rasterMaps.objects.get(pk=idx)
    except recover_image.DoesNotExist:
        recover_image = None
    if recover_image:
        trash_dataset = get_trash_dataset()  
        recover_image.dataset = recover_image.datasetRecover
        recover_image.datasetRecover = None
        recover_image.save()
        response = dataset_list(request, trash_dataset.pk)
        return response

def get_vrt(datasetId):
    dataset = datasets.objects.get(pk=datasetId)
    dataset_imgs = rasterMaps.objects.filter(dataset=dataset)
    vrt_files = ""
    for img in dataset_imgs:
        vrt_files += '"'+settings.MEDIA_ROOT + str(img.destinazione) + '" '
    vrtFileName = os.path.join(settings.MEDIA_ROOT,'warp',dataset.name) + '.vrt'
    buildVrtCmd = 'gdalbuildvrt -overwrite "%s" %s' % (vrtFileName, vrt_files)
    #coverage = GDALRaster(vrtFileName, write=False)
    #dataset.coverage = GDALRaster(vrtFileName, write=False)
    #dataset.save()
    #print (buildVrtCmd, file=sys.stderr)
    #print ("SIZE/SRID:", dataset.coverage.width, dataset.coverage.height,dataset.coverage.srs.srid, file=sys.stderr)
    #os.system(buildVrtCmd)


@login_required(login_url='/warp/login/')
def vrt_dataset(request, dataset):
    get_vrt( dataset )
    response = dataset_list(request, dataset)
    return response


@login_required(login_url='/warp/login/')
def georef_start(request, datasetId = None, idx = None):

    form = UploadImmagineSorgenteForm()
    source = None
    errore = None
    if request.method == 'POST': # crea un nuovo file da editare
        form = UploadImmagineSorgenteForm(request.POST, request.FILES)
        nuova_mappa = rasterMaps()
        nuova_mappa.titolo = request.POST.get('titolo', '')
        nuova_mappa.note = request.POST.get('note', '')
        nuova_mappa.dataset = datasets.objects.get(pk=datasetId)
        nuova_mappa.save()
        nuova_mappa.sorgente = handle_uploaded_file(request.FILES['sorgente'],nuova_mappa.pk)
        nuova_mappa.save()
        source = {
                'item': nuova_mappa,
                'img': nuova_mappa.sorgente,
                'id':nuova_mappa.pk,
                'target': None,
                'download': None,
                'targetSize':[0,0],
                'targetExtent': [0,0,1,1],
                'attribution': nuova_mappa.titolo, 
                'correlazione': None,
                'clipSorgente': None,
                'clipDestinazione': None,
                'dataset': nuova_mappa.dataset
            }
    else: #edita file esistente
        if idx:
            georefItem = rasterMaps.objects.get(pk=idx)
            datasetId =  georefItem.dataset.pk
            
            #check if not yet georeferenced
            if georefItem.webimg:
                webimgRaster = GDALRaster(settings.MEDIA_ROOT + str(georefItem.webimg), write=False)
                extent = [webimgRaster.extent[0],webimgRaster.extent[1],webimgRaster.extent[2],webimgRaster.extent[3]]
                size = [georefItem.webimg.width,georefItem.webimg.height]
            else:
                webimgRaster = ''
                extent = [0,0,1,1]
                size = [0,0]
                
            source = {
                'item': georefItem,
                'img': georefItem.sorgente, 
                'id': georefItem.pk,
                'target': None if not georefItem.webimg else settings.MEDIA_URL + str(georefItem.webimg)+"?dum="+str(randint(1000000,9999999)),
                'download': None if not georefItem.destinazione else settings.MEDIA_URL + str(georefItem.destinazione)+"?dum="+str(randint(1000000,9999999)),
                'targetSize': size,
                'targetExtent': extent,
                'attribution': georefItem.titolo, 
                'correlazione': georefItem.correlazione,
                'clipSorgente': georefItem.clipSorgente,
                'clipDestinazione': georefItem.clipDestinazione,
                'dataset': georefItem.dataset
                }
    return render(request, "warp.html", {'dataset': datasetId, "source": source,"errore":errore, 'form': form, 'settings': settings})


@login_required(login_url='/warp/login/')
def georef_print(request,idx):
    
    georefItem = rasterMaps.objects.get(pk=idx)
    destinazioneImg = str(georefItem.destinazione)
    openlayersImg = str(georefItem.webimg)
    destinazioneFile = settings.MEDIA_ROOT + destinazioneImg
    openlayersFile = settings.MEDIA_ROOT + openlayersImg
    openlayersUrl = settings.MEDIA_URL + openlayersImg
    
    destinazioneRaster = GDALRaster(destinazioneFile, write=False)
    
    target = {
        'url': openlayersUrl+"?dum="+str(randint(1000000,9999999)), 
        'extent': [
                destinazioneRaster.extent[0],
                destinazioneRaster.extent[1],
                destinazioneRaster.extent[2],
                destinazioneRaster.extent[3]
            ],
        'size': [
                destinazioneRaster.width,
                destinazioneRaster.height
            ]
        }
        
    return render(request, "warp_print.html", {"target": target,'dataset': georefItem.dataset,"settings": settings})


@login_required(login_url='/warp/login/')
def georef_apply(request):
    """
    do georef
    """
    
    def execute (cmd):
        """
        execute command and write log
        """
        os.system('echo "%s<br/>\n" >> "%s"  2>&1' % (cmd,logCmdFilename))
        os.system('%s >> "%s"  2>&1' % (cmd,logCmdFilename))
        os.system('echo "<br/>\n<br/>\n" >> "%s"  2>&1' % (logCmdFilename))
    
    if request.is_ajax():
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            postData = json.loads(body_unicode)
            id = json.loads(postData['id'])
            alpha = json.loads(postData['alpha']) == 1
            georefItem = rasterMaps.objects.get(pk=id)
            sorgenteImg = str(georefItem.sorgente)
            destinazioneImg = sorgenteImg[:10] + 'd' + sorgenteImg[11:-4] + '.tif'
            tempImg = sorgenteImg[:10] + 't' + sorgenteImg[11:-4] + '.tif'
            openlayersImg = sorgenteImg[:10] + 'o' + sorgenteImg[11:-4] + '.png'
            sorgenteClip = sorgenteImg[:-4] + '.geojson'
            destinazioneClip = destinazioneImg[:-4] + '.geojson'
            
            #build log file
            logCmd = sorgenteImg[:-4] + '.log'
            logCmdFilename = settings.MEDIA_ROOT + logCmd
            try:
                # cancella il file di log se presente
                os.remove(logCmdFilename)
            except:
                pass
            os.system('touch "%s"' % logCmdFilename)
            logCmdUrl = settings.MEDIA_URL + logCmd
            
            risposta = { 'valida': None, 'esito':logCmdUrl,'geotiff':"", 'estensione': [], 'dest_img': ""}
            
            controlli_sorgente_string = json.loads(postData['controlli_sorgente'])
            controlli_destinazione_string = json.loads(postData['controlli_destinazione'])
            if postData['clip_poligono']:
                clip_poligono_string = json.loads(postData['clip_poligono'])
            else:
                clip_poligono_string = None
                
            controlli_sorgente = json.loads(controlli_sorgente_string)
            controlli_destinazione = json.loads(controlli_destinazione_string)

            features_sorgente = controlli_sorgente['features']
            features_destinazione = controlli_destinazione['features']
            num_controlli = len(features_sorgente)
            correlazione = []
            for i in range(0,num_controlli):
                correlazione.append([[],[]])
            
            for feature in features_sorgente:
                coordinate = feature['geometry']['coordinates']
                indice = feature['properties']['indice'] - 1
                correlazione[indice][0] = coordinate
            
            for feature in features_destinazione:
                coordinate = feature['geometry']['coordinates']
                indice = feature['properties']['indice'] - 1
                correlazione[indice][1] = coordinate
            
            sorgenteFile = settings.MEDIA_ROOT + sorgenteImg
            tempFile = settings.MEDIA_ROOT + tempImg
            destinazioneFile = settings.MEDIA_ROOT + destinazioneImg
            openlayersFile = settings.MEDIA_ROOT + openlayersImg
            sorgenteClipFile = settings.MEDIA_ROOT + sorgenteClip
            destinazioneClipFile = settings.MEDIA_ROOT + destinazioneClip
            
            if os.path.isfile(tempFile):
                os.remove(tempFile)
            
            #print ("\n",sorgenteFile, file=sys.stderr)
            
            if clip_poligono_string:
                # scrivi file json con il poligono di clip
                with open(sorgenteClipFile, 'wt') as out:
                    out.write(clip_poligono_string)
                gdal_clip_cmd = 'gdalwarp -cutline %s '
                    
            gcpString = ""
            gcpStringClip = ""
            altezza_img = georefItem.sorgente.height
            for gcp in correlazione:
                gcpString += "-gcp %s %s %s %s " % (gcp[0][0], altezza_img - gcp[0][1], gcp[1][0], gcp[1][1])
                gcpStringClip += "-gcp %s %s %s %s " % (gcp[0][0], gcp[0][1], gcp[1][0], gcp[1][1])
            
            sorgenteRaster = GDALRaster(sorgenteFile, write=False)
            numero_bande = len(sorgenteRaster.bands)
            #if numero_bande == 1:
            #    bande = '-b 1' #genera errore Band 2 requested, but only bands 1 to 1 available.
            #elif numero_bande == 2:
            #    bande = '-b 1 -b 2'
            #elif numero_bande >= 3:
            #    bande = '-b 1 -b 2 -b 3'
            
            if numero_bande >= 3:
                bande = '-b 1 -b 2 -b 3'

            else:
                bande = ''
                
            if numero_bande < 3:
                expand = '-expand rgb'
            else:
                expand = ''
            
            gdal_translate_cmd = 'gdal_translate %s %s -of GTiff %s "%s" "%s"' % (bande, expand, gcpString, sorgenteFile, tempFile)
            
            metodo = "-tps"
            #metodo = "-order 2"
            
            if clip_poligono_string:
                # scrivi file json con il poligono di clip
                with open(sorgenteClipFile, 'wt') as out:
                    out.write(clip_poligono_string)
                try:
                    os.remove(destinazioneClipFile)
                except:
                    pass
                ogr_clip_cmd = 'ogr2ogr -a_srs EPSG:%s -f "GeoJSON" %s %s "%s" "%s"' % (georefItem.dataset.epsg, gcpStringClip, metodo, destinazioneClipFile, sorgenteClipFile)
                execute(ogr_clip_cmd)
                #post_gdal_warp = 'gdalwarp -r cubic -co COMPRESS=JPEG -co JPEG_QUALITY=75 -overwrite -cutline "%s" -crop_to_cutline "%s" "%s"' % (destinazioneClipFile, destinazioneFile, logCmdFilename)
                clString = '-cutline "%s" -crop_to_cutline' % destinazioneClipFile
            else:
                #post_gdal_warp = None
                clString = ''
                
            if alpha:
                nodata = '-srcnodata "255 255 255"'
            else:
                nodata = ''
            
            gdal_warp_cmd = 'gdalwarp -r cubic %s %s -co COMPRESS=JPEG -co JPEG_QUALITY=75 %s -dstalpha -overwrite -t_srs EPSG:%s "%s" "%s" ' % ( nodata, metodo, clString, georefItem.dataset.epsg, tempFile, destinazioneFile) #
            
            try:
                execute(gdal_translate_cmd)
            except:
                return JsonResponse(risposta)
                
            try:
                execute(gdal_warp_cmd)
            except:
                return JsonResponse(risposta)
            
            try:
                os.remove(tempFile)
            except:
                pass
                
            if os.path.isfile(destinazioneFile):
                georefItem.destinazione = destinazioneImg
                destinazioneRaster = GDALRaster(destinazioneFile, write=False)
                gdal_translate_cmd = 'gdal_translate -of PNG -scale -co worldfile=yes "%s" "%s" ' % ( destinazioneFile, openlayersFile)
                execute(gdal_translate_cmd)
                georefItem.destinazione = destinazioneImg
                georefItem.webimg = openlayersImg
                georefItem.correlazione = json.dumps(correlazione)
                georefItem.save()
                get_vrt(georefItem.dataset.pk)
                
                # scrivi file json con i dati di correlazione
                jsonFileName = settings.MEDIA_ROOT + "warp/" + sorgenteImg[11:-4] + '.json'
                with open(jsonFileName, 'wt') as out:
                    out.write(json.dumps(correlazione))
                
                # carica il clip file json se presente
                if clip_poligono_string:
                    with open(destinazioneClipFile, 'rt') as f:
                        clipjson = f.read()
                    georefItem.clipSorgente = clip_poligono_string
                    georefItem.clipDestinazione = clipjson
                    georefItem.save()
                else:
                    clipjson = ''
                
                
                risposta = { 
                        'valida': True, 
                        'esito': logCmdUrl,
                        'estensione': destinazioneRaster.extent, 
                        'geotiff': settings.MEDIA_URL+destinazioneImg+"?dum="+str(randint(1000000,9999999)), 
                        'dest_img': settings.MEDIA_URL+openlayersImg+"?dum="+str(randint(1000000,9999999)), 
                        'img_dim': [destinazioneRaster.width,destinazioneRaster.height],
                        'clipSorgente': clip_poligono_string,
                        'clipDestinazione': clipjson,
                        'id': id
                    }
            else:
                risposta = { 
                        'valida': None, 
                        'esito':logCmdUrl, 
                        'estensione': [], 
                        'geotiff':"",
                        'dest_img': "",
                        'img_dim': [],
                        'clipSorgente': "",
                        'clipDestinazione': "",
                        'id': 0
                    }
    #logCmdFile.close()
    return JsonResponse(risposta)
