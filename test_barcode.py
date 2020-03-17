from PIL import Image
from pprint import pprint as pp
import barcode
from barcode.writer import ImageWriter


def generate_barcode(ticket_id):
    barcode_class = barcode.get_barcode_class("code39")
    generated_barcode = barcode_class(ticket_id,add_checksum=False, writer=ImageWriter())
    pp(generated_barcode.get_fullcode())
    barcode_filename = generated_barcode.save(
        "barcodes/{}".format(ticket_id), 
        options={
            "background":'white',#"rgba(0,0,0,0)", | darkorange | peru | lightpink | mediumvioletred | lightsalmon | lightcoral
            "foreground":"black",
            "quiet_zone":1,
            "text_distance":1,
            "module_height":8 # default is 15mm
            }
        )
    pp(barcode_filename) ###
    return barcode_filename


def coordinates_centered(fg_barcode,bg_template):
    delta = bg_template.size[1] - fg_barcode.size[1]
    if delta > 0:
        height_offset = int(delta / 2)
        coodinates_centered = (0,height_offset)
    else:
        coodinates_centered = (0,0)
    return coodinates_centered


def merge_barcode(ticket_id, barcode_filename, template_filename):
    ticket_filename = "tickets/{}_ticket.png".format(ticket_id)
    fg_barcode = Image.open(barcode_filename).convert("RGBA")
    bg_template = Image.open(template_filename)
    fg_barcode = fg_barcode.rotate(-90, Image.NEAREST, expand = 1) 
    mult = bg_template.size[1] / fg_barcode.size[1]
    fg_barcode = fg_barcode.resize(
        (
            int(fg_barcode.size[0] * mult),
            int(fg_barcode.size[1] * mult)
        )
    )
    h, w = coordinates_centered(fg_barcode,bg_template)
    bg_template.paste(fg_barcode, (w-50,h), fg_barcode)
    bg_template.save(ticket_filename,format="png")
    pp(ticket_filename)
    return ticket_filename



if __name__=="__main__":
    start_number = 1800
    number_to_print = 1
    template_filename = "templates/blank_bdn_background.png"

    for ticket_id in range(start_number,start_number+number_to_print):
        ticket_id = str(ticket_id).zfill(6)

        barcode_filename = generate_barcode(ticket_id)
        merge_barcode(ticket_id, barcode_filename, template_filename)


