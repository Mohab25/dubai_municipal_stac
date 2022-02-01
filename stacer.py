from datetime import datetime
import string
import random
import pystac
import rasterio
from shapely.geometry import Polygon, mapping, shape

def get_limits(path:str= '')->tuple:
    """
        get the bounding box and the geometry of the image
        
        args:
        ----
        path (str): string representing the path of the image. 
    """
    if path == '':
        raise BaseException('path to image is not given')

    with rasterio.open(path) as ds:
        b = ds.bounds
        bbox = [b.left, b.bottom, b.right, b.top]
        footprint = Polygon([[b.left, b.bottom], [b.left, b.top], [b.right, b.top], [b.right, b.bottom]])
        return (bbox, mapping(footprint))

def create_stac_item(image_path: str, item_id: str = '', image_date:datetime = None, properties: dict = {}):
    """
        creates a stac item out of the provided image
        
        args:
        ----
        image_path (str): the path to the image file.
        item_id (str): a unique name for the item, if empty a random name will be generated.
        image_date (datetime.datetime): the datetime in which the image was captured.
        properties (dict): items extra properties
    """
    if image_date is None:
        image_date = datetime.utcnow()
    b, foot = get_limits(image_path)
    if item_id == '':
        item_id = 'item'+ ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    stac_item = pystac.Item(id=item_id, bbox=b, geometry=foot, datetime=image_date, properties={**properties})
    stac_item.add_asset(key='image', asset= pystac.Asset(href=image_path, media_type = pystac.MediaType.GEOTIFF))
    return stac_item


def create_stac_collection(collection_id:str = '', collection_title:str = '', collection_description='', collection_items: list = [], collection_license='MIT'):
    """
        creates a stac collection to hold stac items.
        
        args:
        ----
        collection_id (str): a unique name for the collection,
            if not provided, a random name will be generated.
        collection_title (str): descriptive title for the collection
            if not provided, the title will be the same as the id.
        collection_description (str): a descriptive text about the
            collection.
        collection_items (list): a list of stac items.
        collection_licence (str): the licence of the collection.
    """
    if collection_items == []:
        raise Exception("can't create a collection from items list")
    
    if collection_id == '':
        collection_id = 'collection'+ ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    
    if collection_title == '':
        collection_title = collection_id

    union_footprint = {'type':'Polygon','coordinates':[]}
    temporal_ext_list = [] 
    for item in collection_items:
        union_footprint = shape(union_footprint).union(shape(item.geometry)) # check stack items methods ->  get shape and get time 
        temporal_ext_list.append(item.datetime)

    collection_bounds = list(union_footprint.bounds)
    collection_spatial_extent = pystac.SpatialExtent(collection_bounds)
    collection_temporal_extent = pystac.TemporalExtent(intervals=sorted(temporal_ext_list))
    collection_extent = pystac.Extent(spatial=collection_spatial_extent, temporal=collection_temporal_extent)
    collection = pystac.Collection(id=collection_id, title=collection_title, description = collection_description, extent=collection_extent, license=collection_license)
    collection.add_items(collection_items)
    return collection

def create_stac_catalog(catalog_id:str = '', catalog_title:str ='', description:str = 'without description', collection: pystac.Collection = None)-> pystac.Catalog:
    """
        cretes a stac catalog and optionally adds a collection to it.

        args:
        ----
        catalog_id (str): a unique name for the catalog,
            if empty, a random name will be generated.
        catalog_title (str): a descriptive title of the catalog,
        if not provided, the id will be used.
        description (str): a descriptive text regarding the catalog.
        collection (pystac.Collection): a child collection, 
        if the collection is empty it returns a catalog 
        without content.

    """
    if catalog_id == '':
        catalog_id = 'catalog'+ ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    
    if catalog_title == '':
        catalog_title = catalog_id

    if collection is None:
        return pystac.Catalog(id=catalog_id, description=description)
    
    Catalog = pystac.Catalog(id=catalog_id, description=description)
    Catalog.add_child(collection)
    return Catalog