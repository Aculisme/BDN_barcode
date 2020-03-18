from PIL import Image
from pprint import pprint as pp
import barcode
import time
from barcode.writer import ImageWriter

# Style imports
from style_options import barcode_style_options


def generate_barcode(ticket_id,**barcode_style):
    """
        Saves a .png barcode file to the /barcodes folder, with a barcode generated according to the ticket ID supplied.
    """
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
    """ 
        Returns the height offset required for a vertically-centered barcode on the left edge of the canvas.
    """
    delta = bg_template.size[1] - fg_barcode.size[1]
    if delta > 0:
        height_offset = int(delta / 2)
        coodinates_centered = (0,height_offset)
    else:
        coodinates_centered = (0,0)
    return coodinates_centered


def merge_barcode(ticket_id, barcode_filename, template_filename,w_offset_mult=0.0):
    """ 
        Merges a barcode from /barcodes with the template ticket background, storing the ticket in /tickets.
    """
    ticket_filename = "tickets/{}.png".format(ticket_id) # _ticket
    fg_barcode = Image.open(barcode_filename).convert("RGBA")
    bg_template = Image.open(template_filename)

    # custom barcode modifications
    fg_barcode = fg_barcode.rotate(-90, Image.NEAREST, expand = 1) 
    mult = bg_template.size[1] / fg_barcode.size[1]
    fg_barcode = fg_barcode.resize(
        (
            int(fg_barcode.size[0] * mult),
            int(fg_barcode.size[1] * mult)
        )
    )
    w, h = fg_barcode.size

    h_offset_centered, w_offset_centered = coordinates_centered(fg_barcode,bg_template)
    # h_offset_final, w_offset_final = int(h_offset_centered - (h * h_offset_mult)), int(w_offset_centered - (w * w_offset_mult))
    w_offset_final = int(w_offset_centered - (w * w_offset_mult))

    # merge and save finished ticket
    bg_template.paste(fg_barcode, (w_offset_final,h_offset_centered), fg_barcode)
    bg_template.save(ticket_filename,format="png")
    pp(ticket_filename)
    return ticket_filename


def upload_to_db(ticket_id):
    """
        (Will) add the ticket ID to a remote database using SQL.
    """
    pass


if __name__=="__main__":
    # ticket style options
    start_number = 1900
    number_to_print = 10
    template_filename = "templates/bdn_2020_background_HQ_small.png"
    barcode_style = barcode_style_options['peach']
    w_offset_mult = 0.05

    ts = time.time() # start time

    for ticket_id in range(start_number,start_number+number_to_print):
        ticket_id = str(ticket_id).zfill(6)

        barcode_filename = generate_barcode(ticket_id,**barcode_style)
        merge_barcode(ticket_id, barcode_filename, template_filename,w_offset_mult=w_offset_mult)
    
    pp(time.time()-ts) # print end time