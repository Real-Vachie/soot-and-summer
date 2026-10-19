# Pet sprites (the app's own art, sitting, hats on), logo, pack art and room photos for docs/media.
from pathlib import Path
from PIL import Image
H = Path.home(); F = H/'Projects/summer-phone/promo/frames'; S = H/'Projects/summer-phone/store'; M = Path('docs/media')
PETS = 'summer_none soot_none lab_none raccoon_crown redpanda_beanie fox_cowboy skunk_bow possum_party lynx_tophat serval_flowers ' \
       'caracal_cap snowleopard_beanie sandcat_party corgi_cap husky_beanie pug_party wolf_crown dachshund_bow dalmatian_tophat ' \
       'shiba_flowers beagle_cowboy arcticfox_beanie greyhound_cap'.split()
def fit(im, w, h=None):
    im = im.copy(); im.thumbnail((w, h or w), Image.LANCZOS); return im
for p in PETS:
    im = Image.open(F/f'{p}_0.png').convert('RGBA'); im = im.crop(im.getbbox())
    fit(im, 200).save(M/f'pets/{p.split("_")[0]}.webp', quality=85)
fit(Image.open(S/'icon-512.png'), 256).save(M/'app-icon.png')  # the brand mark is copied by hand from summer-phone promo/brand/out
for p in ('cat_pack', 'dog_pack'): fit(Image.open(S/f'packs/{p}.png'), 360).save(M/f'{p}.webp', quality=85)
O = H/'Projects/sns-shorts/out/photos'
room = Image.open(O/'group_a_16x9.png').convert('RGB'); room = room.crop((0, int(room.height * .38), room.width, room.height))  # below its title
fit(room, 1600).save(M/'room.webp', quality=78)
fit(Image.open(O/'group_b_4x5.png').convert('RGB'), 800, 1000).save(M/'group.webp', quality=80)
