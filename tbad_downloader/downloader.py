
import refine.refine as refine
import requests
import hashlib
import json
import csv
import os
import re


#############################################


dataset_e = []
dataset_p = []


#############################################


def generate_sha(fpath):
    sha1 = hashlib.sha1()
    f = open(fpath, 'rb')
    try:
        clean = re.sub("[\n\r]+", "", f.read());
        sha1.update(clean)
    finally:
        f.close()
    return sha1.hexdigest()


def add_to_big_dataset(dataset_id, pos, dataset_row):
    if dataset_id in list_points:
        if pos == 0 and len(dataset_p) == 0:
            dataset_p.append(dataset_row)
        elif pos > 0:
            dataset_p.append(dataset_row)
    else:
        if pos == 0 and len(dataset_e) == 0:
            dataset_e.append(dataset_row)
        elif pos > 0:
            dataset_e.append(dataset_row)


def write_big_dataset(dataset_name, dataset_values):
    with open(dataset_folder + dataset_name + '.csv', 'wb') as f:
        writ = csv.writer(f)
        writ.writerows(dataset_values)
    print "- Big dataset: " + dataset_name + " saved."


def write_dataset(dataset_id, dataset_values, add_function):
    with open(dataset_folder + dataset_id + '_dataset.csv', 'wb') as f:
        ec_file_list = dataset_values.split('\n')
        writ = csv.writer(f)
        for x in range(0, len(ec_file_list) - 1):
            d = ec_file_list[x]
            d = d.replace('\t ', '\t')
            da = d.split('\t')
            add_function(dataset_id, x, da)
            writ.writerow(da)
    print " * Dataset: " + dataset_id + " updated !"


def download_dataset(fpath, dataset_id, dataset_url):
    with open(fpath, 'wb') as handle:
        response = requests.get(dataset_url, stream=True)
        for block in response.iter_content(1024):
            handle.write(block)
    print "- Downloaded Dataset: " + dataset_id


def get_project_options(identifier):
    idjson = None
    for i in operations_create:
        if identifier in operations_create[i]:
            idjson = i
            break
    with open('../refine_op/' + idjson + '.json', 'r') as handle:
        return json.loads(handle.read())


def detect_dataset(old_path, new_path):
    if os.path.exists(new_path):
        if generate_sha(old_path) != generate_sha(new_path):
            os.remove(old_path)
            os.rename(new_path, old_path)
            print " * Updating data for dataset ..."
        else:
            os.remove(new_path)
            print " * Old data detected. Clean and do nothing."
            return True
    else:
        print " * Previous version not found. Saved."
    return False


#############################################


# Culture / Entertainment
datasets_ce = {
    '206974': 'http://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.csv',
    '212504': 'http://datos.madrid.es/egob/catalogo/212504-0-agenda-actividades-deportes.csv',
    # '200652': 'http://datos.madrid.es/egob/catalogo/200652-1-areas-infantiles.csv',
    # '200637': 'http://datos.madrid.es/egob/catalogo/200637-1-areas-mayores.csv',
    # '206717': 'http://datos.madrid.es/egob/catalogo/206717-0-agenda-eventos-bibliotecas.csv',
    '200186': 'http://datos.madrid.es/egob/catalogo/200186-0-polideportivos.csv',
    # '212808': 'http://datos.madrid.es/egob/catalogo/212808-0-espacio-deporte.csv',
    # '200215': 'http://datos.madrid.es/egob/catalogo/200215-0-instalaciones-deportivas.csv',
    '210227': 'http://datos.madrid.es/egob/catalogo/210227-0-piscinas-publicas.csv',
    # '209426': 'http://datos.madrid.es/egob/catalogo/209426-0-templos-catolicas.csv',
    # '209434': 'http://datos.madrid.es/egob/catalogo/209434-0-templos-otros.csv',
    # '208862046': 'http://datos.madrid.es/egob/catalogo/208862-7650046-ocio_salas.csv',
    # '208862164': 'http://datos.madrid.es/egob/catalogo/208862-7650164-ocio_salas.csv',
    # '208862180': 'http://datos.madrid.es/egob/catalogo/208862-7650180-ocio_salas.csv',
    # '217921': 'http://datos.madrid.es/egob/catalogo/217921-0-salas-estudio.csv',
    '200761': 'http://datos.madrid.es/egob/catalogo/200761-0-parques-jardines.csv',
    # '300028': 'http://datos.madrid.es/egob/catalogo/300028-10037314-agenda-turismo.xml'
}


# Buildings / Centers
datasets_bc = {
    # '201747': 'http://datos.madrid.es/egob/catalogo/201747-0-bibliobuses-bibliotecas.csv',
    '212763': 'http://datos.madrid.es/egob/catalogo/212763-0-biblioteca-universitaria.csv',
    '200304': 'http://datos.madrid.es/egob/catalogo/200304-0-centros-culturales.csv',
    # '205244': 'http://datos.madrid.es/egob/catalogo/205244-0-infancia-familia-adolescentes.csv',
    # '200342': 'http://datos.madrid.es/egob/catalogo/200342-0-centros-dia.csv',
    # '209094': 'http://datos.madrid.es/egob/catalogo/209094-0-servicios-sociales.csv',
    # '200337': 'http://datos.madrid.es/egob/catalogo/200337-0-centros-mayores.csv',
    # '205712': 'http://datos.madrid.es/egob/catalogo/205712-0-servicios-sociales.csv',
    # '205732': 'http://datos.madrid.es/egob/catalogo/205732-0-servicios-sociales.csv',
    # '206117': 'http://datos.madrid.es/egob/catalogo/206117-0-entidades-participacion-ciudadan.csv',
    # '202781': 'http://datos.madrid.es/egob/catalogo/202781-0-entidades-participacion-ciudadan.csv',
    # '214440': 'http://datos.madrid.es/egob/catalogo/214440-0-farmacias-guardia.csv',
    # '202162': 'http://datos.madrid.es/egob/catalogo/202162-0-instalaciones-accesibles-municip.csv',
    # '202180': 'http://datos.madrid.es/egob/catalogo/202180-0-instalaciones-accesibles-no-muni.csv',
    # '216619': 'http://datos.madrid.es/egob/catalogo/216619-0-wifi-municipal.csv',
    # '202311': 'http://datos.madrid.es/egob/catalogo/202311-0-colegios-publicos.csv',
    # '202318': 'http://datos.madrid.es/egob/catalogo/202318-0-escuelas-infantiles.csv',
    # '212790': 'http://datos.madrid.es/egob/catalogo/212790-0-centros-educacion.csv',
    # '212904': 'http://datos.madrid.es/egob/catalogo/212904-0-centros-ensenanza.csv',
    # '212816': 'http://datos.madrid.es/egob/catalogo/212816-0-investigacion.csv',
    '211642': 'http://datos.madrid.es/egob/catalogo/211642-0-bomberos-parques.csv',
    '201544': 'http://datos.madrid.es/egob/catalogo/201544-0-centros-salud.csv',
    '212769': 'http://datos.madrid.es/egob/catalogo/212769-0-atencion-medica.csv',
    # '202105': 'http://datos.madrid.es/egob/catalogo/202105-0-mercadillos.csv',
    # '200967': 'http://datos.madrid.es/egob/catalogo/200967-0-mercados.csv',
    # '300048': 'http://datos.madrid.es/egob/catalogo/300048-0-ancianos-residencias-apartamento.csv',
    '207044': 'http://datos.madrid.es/egob/catalogo/207044-0-oficina-policia.csv',
    # '203166': 'http://datos.madrid.es/egob/catalogo/203166-0-universidades-educacion.csv',
    # '212774': 'http://datos.madrid.es/egob/catalogo/212774-0-atencion-social.csv',
    # '212841': 'http://datos.madrid.es/egob/catalogo/212841-0-oficinas-correos.csv',
    # '212846': 'http://datos.madrid.es/egob/catalogo/212846-0-oficinas-correos.csv',
    # '205736': 'http://datos.madrid.es/egob/catalogo/205736-0-servicios-sociales.csv'
}


# Viability
datasets_v = {
    # '21241109': 'http://datos.madrid.es/egob/catalogo/212411-9-madrid-avisa.csv',
    # '21241111': 'http://datos.madrid.es/egob/catalogo/212411-11-madrid-avisa.csv',
    # '211346': 'http://datos.madrid.es/egob/catalogo/211346-0-estaciones-acusticas.xls',
    # '215885': 'http://datos.madrid.es/egob/catalogo/215885-0-contaminacion-ruido.txt',
    # '212629': 'http://datos.madrid.es/egob/catalogo/212629-0-estaciones-control-aire.xls',
    # '212531': 'http://datos.madrid.es/egob/catalogo/212531-7916318-calidad-aire-tiempo-real.txt',
    # '209799': 'http://datos.madrid.es/egob/catalogo/209799-3-contenedores_pilas_marquesinas.csv',
    # '204410': 'http://datos.madrid.es/egob/catalogo/204410-1-contenedores-ropa.csv',
    # '212616': 'http://datos.madrid.es/egob/catalogo/212616-18-policia-estadisticas.xls',
    # '200284': 'http://datos.madrid.es/egob/catalogo/200284-0-puntos-limpios.csv'
}


# Transport
datasets_t = {
    # '202625': 'http://datos.madrid.es/egob/catalogo/202625-0-aparcamientos-publicos.csv',
    # '202584': 'http://datos.madrid.es/egob/catalogo/202584-0-aparcamientos-residentes.csv',
    # '208083': 'http://datos.madrid.es/egob/catalogo/208083-0-estacionamiento-pmr.xls',
    # '208789': 'http://datos.madrid.es/egob/catalogo/208789-7648433-transportes-emt-xls.xls',
    # '202087': 'http://datos.madrid.es/egob/catalogo/202087-0-trafico-intensidad.xml',
    # '202468': 'http://datos.madrid.es/egob/catalogo/202468-0-intensidad-trafico.zip',
    # '202062': 'http://datos.madrid.es/egob/catalogo/202062-0-trafico-incidencias-viapublica.xml',
    # '202974': 'http://datos.madrid.es/egob/catalogo/202974-0-trafico-semaforos.xml',
    # '208426': 'http://datos.madrid.es/egob/catalogo/208426-0-trafico-semaforos-no-comunican.xml',
    # '208327': 'http://datos.madrid.es/egob/catalogo/208327-1-transporte-bicicletas-bicimad.csv'
}

# List to create a unified dataset about datasets with same properties
list_points = ['200186', '200304', '200761', '201544', '207044', '210227', '211642', '212763', '212769']
list_events = ['206974', '212504']

# Relations between create refine scripts and datasets.
# For reuse the same create script.
operations_create = {
    'creation_one': [
        '200637', '200652', '214440', '208327'
    ],
    'creation_five': [
        '200186', '206974', '210227', '212504', '200761', '201747', '212763',
        '200304', '211642', '201544', '212769', '202105', '200967', '207044',
        '212841', '212846', '205736', '200284'
    ],
    'creation_211346': ['211346'],
    'creation_212629': ['212629'],
    'creation_208789': ['208789']
}

datasets = datasets_ce.copy()
datasets.update(datasets_bc)
datasets.update(datasets_v)
datasets.update(datasets_t)

# Folder to save all datasets created
dataset_folder = '/tmp/datasets/'


#############################################

# Create datasets folder if it does not exist
if not os.path.exists(dataset_folder):
    os.makedirs(dataset_folder)

print '\nTBADDownloader has started.'
print '\n * Checking (' + str(len(datasets.keys())) + ') datasets ...\n'

# Iterate over datasets
for i in datasets.keys():

    # Save new data or save in the old dataset
    ext = os.path.split(datasets[i])[-1].split('.')[-1]
    name_path = dataset_folder + i + '.' + ext
    name_new_path = dataset_folder + 'new_' + i + '.' + ext
    file_path = name_path
    if os.path.exists(name_path):
        file_path = name_new_path

    # Download dataset with the dict url
    download_dataset(file_path, i, datasets[i])

    # Check if it is old or new with sha
    if not detect_dataset(name_path, name_new_path):

        # Get Refine Options (create script)
        opt = get_project_options(i)
        r = refine.Refine()
        p = r.new_project(name_path, opt)

        # Apply Refine Operations from json file
        p.apply_operations('../refine_op/clean_' + i + '.json')

        # Write new Dataset with cleaned data
        write_dataset(i, p.export_rows(format='tsv'), add_to_big_dataset)

        # Delete Refine Project to clean memory
        p.delete_project()

    else:

        # Write new Dataset with previous data
        with open(dataset_folder + i + '_dataset.csv', 'r') as f:
            ec_file_list = f.read().split('\r\n')
            for x in range(0, len(ec_file_list) - 1):
                d = ec_file_list[x]
                d = d.replace('"','')
                d = d.replace(', ','__ ').replace(',','\t').replace('__', ',')
                d = d.split('\t')
                add_to_big_dataset(i, x, d)

# Write or skip updated unified csv
write_big_dataset('dataset_points', dataset_p)
write_big_dataset('dataset_events', dataset_e)

print '\nTBADDownloader has finished.\n'
