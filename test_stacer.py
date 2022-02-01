from pathlib import Path
from datetime import datetime
import pystac
import sys 
sys.path.append("..")
import stacer
#from ..dubai_muncipal_package import stacer

item1 = stacer.create_stac_item('dubai_ast_16oct02_geo_reprojected.tif', image_date = datetime.strptime('Oct 16 2002','%b %d %Y'))
item2 = stacer.create_stac_item('dubai_ast_17nov08_geo_reprojected.tif', image_date = datetime.strptime('Nov 17 2008','%b %d %Y'))
collection = stacer.create_stac_collection(collection_items=[item1, item2])
catalog = stacer.create_stac_catalog(collection=collection)
catalog.normalize_hrefs(str(Path(__file__).parent.joinpath('test_folder')))
catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

def test_catalog_creation():
    cat = Path(__file__).parent.joinpath('test_folder/catalog.json')
    assert cat.is_file()

def test_collection_creation():
    col = Path(__file__).parent.joinpath(f'test_folder/{collection.id}')
    assert col.is_dir()

def test_item_creation():
    i = Path(__file__).parent.joinpath(f'test_folder/{collection.id}/{item1.id}/{item1.id}.json')
    assert i.is_file()


test_catalog_creation()
test_collection_creation()
test_item_creation()