# usage:
#   python letters.py input.file
#   logs to file's in the output directory

import datetime
import lob
import os
import sys

sys.path.insert(0, os.path.abspath(__file__+'../../..'))

lob.api_key = 'test_fc26575412e92e22a926bc96c857f375f8b'
# Input check
if len(sys.argv) < 2:
    print("Please provide an input FILE file as an argument.")
    print("usage: python letter.py <FILE>.txt")
    sys.exit(1)

input_filename = sys.argv[1]
if os.path.exists(input_filename):
            fo = open(input_filename, "r")

            Name = fo.readline().split(': ')[1].upper()
            Addr1 = fo.readline().split(': ')[1].upper()
            Addr2 = fo.readline().split(': ')[1].upper()
            City = fo.readline().split(': ')[1].upper()
            State = fo.readline().split(': ')[1].upper()
            Contry = fo.readline().split(': ')[1].upper()
            Zip = fo.readline().split(': ')[1]
            Message = fo.readline().split(': ')[1]

            fo.close()
else:
    print "Input file is not exist!\nUsage: python [filename].py -i <inputFile>"
    os._exit(-1)
# TODO: Create your from_address
try:
    from_address = lob.Address.create(
        name=Name,
        address_line1=Addr1,
        address_line2=Addr2,
        address_city=City,
        address_state=State,
        address_zip=Zip,
        address_country=Contry,
    )
except Exception as e:
    print('Error: ' + str(e))
    print('Failed to create from_address.')
    sys.exit(1)

errors_file_fields = ['error'] #??

# create the output directory,
output_dir = os.path.join('.',  'output')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

try:
    output_dir = os.path.join(output_dir, timestamp)
    os.mkdir(output_dir)
except Exception as e:
    print('Error: ' + str(e))
    print('Failed to create output directory. Aborting all sends.')
    sys.exit(1)

# output file names
success_filename = os.path.join(output_dir, 'success.txt')
errors_filename = os.path.join(output_dir, 'errors.txt')

with open('letter.html', 'r') as html_file:
    letter_html = html_file.read()

try:
    if True:
        with open(input_filename, 'r') as input, \
         open(success_filename, 'w') as success, \
         open(errors_filename, 'w') as errors:

            # Print mode to screen
            mode = lob.api_key.split('_')[0]
            print('Sending letters in ' + mode.upper() + ' mode.')

            try:
                letter = lob.Letter.create(
                    #description='Bill for ' + row['name'],
                    metadata={
                        'message': Message,
                        'file':      input_filename
                    },
                    from_address=from_address,
                    to_address={
                        'name':          'DIANNE FEINSTEIN',
                        'address_line1': '331 HART SENATE',
                        'address_line2': 'OFFICE BUILDING',
                        'address_city':  'WASHINGTON',
                        'address_zip':   '20510',
                        'address_state': 'DC',
                        'address_country':'US'
                    },
                    file=letter_html,
                    merge_variables={
                        'date':   datetime.datetime.now().strftime("%m/%d/%Y"),
                        'name':   Name,
                        'message': Message
                    },
                    color=True
                )
                print('url:'+letter.url)
            except Exception as e:
                error_row = {'error': e}
                errors.write(error_row)
                sys.stdout.write('E')
                sys.stdout.flush()
            else:
                success.write(letter.url)

                # Print success
                #sys.stdout.write('.')
                sys.stdout.flush()


except Exception as e:
    print('Error: ' + str(e))
    sys.exit(1)
