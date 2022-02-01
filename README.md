# Dubai_municipal_stac

package for generating stac catalog for Dubai municipality, visit https://stacspec.org/

# Implementation

## Methods

### get_limits

~~~py
def get_limits(path:str= '')->tuple:
~~~

get the bounding box and the geometry of the image

~~~bash
args:
----
path (str): string representing the path of the image. 
~~~

### create_stac_item

~~~py
def create_stac_item(image_path: str, item_id: str = '', image_date:datetime = None, properties: dict = {}):
~~~

creates a stac item out of the provided image

~~~bash

args:
----
image_path (str): the path to the image file.
item_id (str): a unique name for the item, if empty a random name will be generated.
image_date (datetime.datetime): the datetime in which the image was captured.
properties (dict): items extra properties
~~~


### create_stac_collection

~~~py
def create_stac_collection(collection_id:str = '', collection_title:str = '', collection_description='', collection_items: list = [], collection_license='MIT'):
~~~

creates a stac collection to hold stac items.
        
~~~bash
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
~~~

### create_stac_catalog

~~~py
def create_stac_catalog(catalog_id:str = '', catalog_title:str ='', description:str = 'without description', collection: pystac.Collection = None)-> pystac.Catalog:
~~~

cretes a stac catalog and optionally adds a collection to it        

~~~bash
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

~~~
