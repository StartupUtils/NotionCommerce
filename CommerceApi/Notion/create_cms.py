from CommerceApi.Notion import content, orders, products
from CommerceApi.Notion.manager import NotionClient
from CommerceApi.config import Config
from CommerceApi.utils.mongo import Mongoify
import time
import uuid

class BuildStep:
    def __init__(self, method, *args):
        self.method = method
        self.args = args
        self.callback = None
        
    async def execute(self):
        result = self.method(*self.args)
        if self.callback:
            await self.callback(result)

class CMSBuilder:
    def __init__(self):
        self.mongo_client = Mongoify
        self.base_page_id = Config.base_page_id
        self.build_queue = []
        self.parent = {
            "type": "page_id",
            "page_id": self.base_page_id
        }

    async def maybe_create_cms(self) -> None:
        if not await self.cms_already_built():
            await self.build()
        else:
            print("cms built")

    async def cms_already_built(self) -> bool:
        result = await Mongoify.find_one("component_config", {"parent_id": self.base_page_id})
        print(result)
        if result:
            return True
        return False

    async def build(self):
        self.create_order_block()
        self.create_order_table()
        self.create_product_block()
        self.create_product_table()
        for command in self.build_queue:
            time.sleep(.3)
            await command.execute()
            
    def create_order_block(self):
        data = content.order_content_block
        method = NotionClient.append_block_children
        self._add_build_step(method, self.base_page_id, data)
    
    def create_product_block(self):
        data = content.product_content_block
        method = NotionClient.append_block_children
        self._add_build_step(method, self.base_page_id, data)

    def create_order_table(self):
        data = orders.orders_schema(self.parent)
        method = NotionClient.create_database
        build_step = self._add_build_step(method, data)
        build_step.callback = self.handle_order_callback

    def create_product_table(self):
        data = products.products_schema(self.parent)
        method = NotionClient.create_database
        build_step = self._add_build_step(method, data)
        build_step.callback = self.handle_product_callback

    def _add_build_step(self, method, *args):
        step = BuildStep(method, *args)
        self.build_queue.append(step)
        return step

    async def handle_order_callback(self, result):
        data = result.dict()
        data["component_name"] = "order_database"
        data["parent_id"] = result.parent.id
        await Mongoify.update("component_config", {"component_name": "order_database"}, data)

    async def handle_product_callback(self, result):
        data = result.dict()
        data["component_name"] = "product_database"
        data["parent_id"] = result.parent.id
        print(data)
        await Mongoify.update("component_config", {"component_name": "product_database"}, data)

