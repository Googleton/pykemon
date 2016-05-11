import pygame as pg;
import json;
import Tile;
import BasicNPC;

class World:

    img_bg = pg.image.load("resources/map/map.png");
    tileset_image = pg.image.load("resources/tile/tileset.png");
    entities = pg.sprite.LayeredUpdates();
    tiles = [];
    width, height = 20, 20;

    def __init__(self, game):
        self.all_tiles = {};
        self.randomNumberDebug = 5;
        self.tileset_image = pg.image.load("resources/tile/tileset.png");

        self.loadWorld(game);
        print("World Initialized !");

    def update(self, events, world, game):
        for e in self.entities :
            e.update(events, world, game);

    def render(self, display, game):
        for e in self.entities :
            display.blit(e.image, game.camera.apply(e));

    def loadWorld(self, game):
        global width, height;
        #Chargement des donnees
        mapData = open("resources/map/mapData.json").read();
        jsonData = json.loads(mapData);
        self.width = jsonData["width"];
        self.height = jsonData["height"];
        layers = jsonData["layers"];
        tilesets = jsonData["tilesets"];

        for tileset in tilesets :
            tile_id = 1;
            print("Loading new tileset ...");
            for y in range(0, tileset["imageheight"], 16) :
                for x in range(0, tileset["imagewidth"], 16) :
                    rect = pg.Rect(x, y, 16, 16);
                    tile = self.tileset_image.subsurface(rect);
                    self.all_tiles[tile_id] = tile;
                    tile_id += 1;

        for layer in layers:
            print("Adding new layer :", layer["name"]);
            if layer["name"] == "visibleLayer" :
                data = layer["data"];
                layerHeight = layer["height"];
                layerWidth = layer["width"];
                data_index = 0;
                for y in range(0, layerHeight):
                    for x in range(0, layerWidth):
                        tileID = data[data_index];
                        #On ne veux pas ajouter les tiles avec un ID de 1 ou 0
                        if tileID > 1 :
                            tile = Tile.Tile(x * 16, y * 16, tileID, self)
                            tile.rect.topleft = (x * 16, y * 16);
                            self.entities.add(tile);
                        data_index += 1;
            if layer["name"] == "collisionLayer" :
                data = layer["data"];
                layerHeight = layer["height"];
                layerWidth = layer["width"];
                data_index = 0;
                for y in range(0, layerHeight):
                    for x in range(0, layerWidth):
                        #On verifie que la tile n'est pas vide pour ne pas charger des collisions inexistantes
                        tileID = data[data_index];
                        if tileID > 0 :
                            tile = self.tileAt(x*16,y*16);
                            if type(tile) is Tile.Tile :
                                tile.collider = True;
                                tile.occupied = True;
                        data_index += 1;

        #Chargement des NPC du jeu.
        tileData = open("resources/map/tileData.json").read();
        jsonTileData = json.loads(tileData);
        npcs = jsonTileData["npc"];
        teleporters = jsonTileData["teleporters"];
        print("Adding NPCs ..");
        for npc in npcs:
            npcX = npc["x"];
            npcY = npc["y"];
            new_npc = BasicNPC.BasicNPC(npcX * 16, npcY * 16);
            new_npc.dialog = npc["dialog"];
            new_npc.texture = pg.image.load("resources/" + npc["texture"]);
            new_npc.type = npc["type"];
            new_npc.name = npc["name"];
            if npc["hasPath"] == 1 :
                new_npc.hasPath = True;
                paths = npc["path"];
                for path in paths:
                    new_npc.path.append((path["x"], path["y"]))
            if new_npc.type == "trainer" :
                new_npc.createTeam(npc["team"], game);

            self.entities.add(new_npc);

        print("Adding teleports ...");
        for teleporter in teleporters :
            teleportX = teleporter["teleX"];
            teleportY = teleporter["teleY"];
            tileX = teleporter["x"];
            tileY = teleporter["y"];
            tile = self.tileAt(tileX * 16, tileY * 16);
            if type(tile) is Tile.Tile :
                tile.teleporter = True;
                tile.teleportX = teleportX;
                tile.teleportY = teleportY;

    def tileAt(self, x, y):
        for e in self.entities :
            if type(e) is Tile.Tile or type(e) is BasicNPC.BasicNPC :
                if e.rect.x/16 == x/16 and e.rect.y/16 == y/16 :
                    return e;
        return False;

    def interact(self, x, y, entity, game, player):
        for e in self.entities :
            if type(e) is BasicNPC.BasicNPC :
                if e.rect.x/16 == x/16 and e.rect.y/16 == y/16 :
                    e.interact(entity, game, player);
                    return True;
        entity.canInteract = True;
        return False;


