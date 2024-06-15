class Tilemap:
    def __init__(self, game, tile_size=8):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(15):
            self.tilemap[f'{9+i};15'] = {'pos': (9 + i, 15), 'type': 'temp', 'variant': 0}
            self.tilemap[f'22;{8+i}'] = {'pos': (22, 8 + i), 'type': 'temp', 'variant': 0}

    def render(self, surf):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.block, tile['pos'])

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.block, (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))
