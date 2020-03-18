from PIL import Image
from pprint import pprint as pp
import barcode
from barcode.writer import ImageWriter

# Style imports
from style_options import barcode_style_options


def generate_barcode(ticket_id,**barcode_style):
    barcode_class = barcode.get_barcode_class("code39")
    generated_barcode = barcode_class(ticket_id,add_checksum=False, writer=ImageWriter())
    pp(generated_barcode.get_fullcode())
    barcode_filename = generated_barcode.save(
        filename="barcodes/{}".format(ticket_id), 
        options = barcode_style
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


def merge_barcode(ticket_id, barcode_filename, template_filename,w_offset_mult=0):
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
    w_offset = int(w*w_offset_mult)
    bg_template.paste(fg_barcode, (w-w_offset,h), fg_barcode)
    bg_template.save(ticket_filename,format="png")
    pp(ticket_filename)
    return ticket_filename



if __name__=="__main__":
    start_number = 1800
    number_to_print = 1
    # template_filename = "templates/blank_bdn_background.png"
    template_filename = "templates/flipped_blank_bdn_background.png"

    barcode_style = barcode_style_options['cotton_candy']
    pp(barcode_style)
    for ticket_id in range(start_number,start_number+number_to_print):
        ticket_id = str(ticket_id).zfill(6)

        barcode_filename = generate_barcode(ticket_id,**barcode_style)
        
        merge_barcode(ticket_id, barcode_filename, template_filename,w_offset_mult=0.0)


