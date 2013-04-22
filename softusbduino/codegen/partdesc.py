import xml.etree.ElementTree as ET
from path import path

'''
experiment with Partdescriptionfiles
'''

def main():
    PATH=path(__file__).parent.parent.parent / 'Partdescriptionfiles'
    #print PATH
    
    for x in PATH.files('ATmega*.xml'):
    #    print x
        tree = ET.parse(x)
        root = tree.getroot()
    #    print root[0]
        AVRPART=root
        IO_MODULE=AVRPART.find('IO_MODULE')
        USART0= IO_MODULE.find('USART0')
        if USART0:
            regs= USART0.find('LIST').text.strip('[]').split(':')
            adr= USART0.find('UDR0').find('MEM_ADDR').text
            if 'C6' not in adr:
                print x
    #        print USART0.find('TEXT').text
        
    #    for country in root.findall('ADCSRA'):
    #        print country
            
            
            
            
            
            
            
            