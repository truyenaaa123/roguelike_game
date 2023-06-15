import pygame

def import_image_sheet(paths, size, colorkey, scale = 1, rotation = 0, limit_width_size =0, limit_height_size = 0, width_cut=0, height_cut=0):
    surface_list = []
    for path in paths:
        sheet = pygame.image.load(path).convert_alpha()
        rect = sheet.get_rect()
        for col in range((rect.height - limit_height_size)//size[1]):
            for row in range((rect.width - limit_width_size)//size[0]):
                image_surf = pygame.Surface(size).convert_alpha() 
                image_surf.blit(sheet, (0,0), (row*size[0], col*size[1], size[0], size[1]))
                image_surf = pygame.transform.scale(image_surf, (int(size[0]*scale), int(size[1]*scale)))
                image_surf = image_surf.subsurface(pygame.Rect(width_cut, height_cut, int(size[0]*scale) - width_cut*2, int(size[1]*scale)- height_cut*2))
                image_surf = pygame.transform.rotate(image_surf, rotation)
                image_surf.set_colorkey(colorkey)
                surface_list.append(image_surf)
    return surface_list

