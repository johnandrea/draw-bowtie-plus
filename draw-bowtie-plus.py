#!/usr/bin/python3

"""
Convert a genealogy gedcom file into a format for display via graphvis dot file.
The display is of the selected person's ancestors, plus descendants of the
person's grandparents.

Tyoically used for ancestors and cousins.
Can also be for parents and all their descendents.
etc.

This code is released under the MIT License: https://opensource.org/licenses/MIT
Copyright (c) 2022 John A. Andrea
v1.2
Mo support provided.
"""

import sys
import re
import argparse
import importlib.util
import os


def load_my_module( module_name, relative_path ):
    """
    Load a module in my own single .py file. Requires Python 3.6+
    Give the name of the module, not the file name.
    Give the path to the module relative to the calling program.
    Requires:
        import importlib.util
        import os
    Use like this:
        readgedcom = load_my_module( 'readgedcom', '../libs' )
        data = readgedcom.read_file( input-file )
    """
    assert isinstance( module_name, str ), 'Non-string passed as module name'
    assert isinstance( relative_path, str ), 'Non-string passed as relative path'

    file_path = os.path.dirname( os.path.realpath( __file__ ) )
    file_path += os.path.sep + relative_path
    file_path += os.path.sep + module_name + '.py'

    assert os.path.isfile( file_path ), 'Module file not found at ' + str(file_path)

    module_spec = importlib.util.spec_from_file_location( module_name, file_path )
    my_module = importlib.util.module_from_spec( module_spec )
    module_spec.loader.exec_module( my_module )

    return my_module


def get_program_options():
    results = dict()

    orientations = [ 'tb', 'lr', 'bt', 'rl' ]

    results['format'] = 'dot'
    results['infile'] = None
    results['personid'] = None
    results['title'] = None
    results['iditem'] = 'xref'
    results['reverse'] = False
    results['orientation'] = 'tb'
    results['ancestors'] = 100
    results['descendents'] = 2
    results['from'] = 2
    results['dates'] = False
    results['libpath'] = '.'

    arg_help = 'Create a bowtie chart with more options.'
    parser = argparse.ArgumentParser( description=arg_help )

    # only using dot output
    #formats = [results['format'], 'dot', 'json']
    #arg_help = 'Output format. One of: ' + str(formats) + ', Default: ' + results['format']
    #parser.add_argument( '--format', default=formats, choices=formats, type=str, help=arg_help )

    arg_help = 'How to find the reference person. Default is the gedcom id "xref".'
    arg_help += ' Othewise choose "exid", "refnum", etc.'
    parser.add_argument( '--iditem', default=results['iditem'], type=str, help=arg_help )

    arg_help = 'Title to add to graph. Default is none.'
    parser.add_argument( '--title', default=results['title'], type=str, help=arg_help )

    arg_help = 'Show dates along with the names.'
    parser.add_argument( '--dates', default=results['dates'], action='store_true', help=arg_help )

    arg_help = 'Number of generations of ancestors. Default: ' + str(results['ancestors'])
    parser.add_argument( '--ancestors', default=results['ancestors'], type=int, help=arg_help )

    arg_help = 'Number of generations of descendents of grandparents.'
    arg_help += ' Default: ' + str(results['descendents'])
    parser.add_argument( '--descendents', default=results['descendents'], type=int, help=arg_help )

    arg_help = 'Descendents from this many generations back from start.'
    arg_help += ' Default: ' + str(results['from'])
    parser.add_argument( '--fromgen', default=results['from'], type=int, help=arg_help )

    # in dot files, change direction of the arrows
    arg_help = 'For dot file output, reverse the order of the links.'
    parser.add_argument( '--reverse-arrows', default=results['reverse'], action='store_true', help=arg_help )

    arg_help = 'Orientation of the output dot file tb=top-bottom, lt=left-right, etc. Default:' + results['orientation']
    parser.add_argument( '--orientation', default=results['orientation'], type=str, help=arg_help )

    # maybe this should be changed to have a type which better matched a directory
    arg_help = 'Location of the gedcom library. Default is current directory.'
    parser.add_argument( '--libpath', default=results['libpath'], type=str, help=arg_help )

    arg_help = 'Input GEDCOM file.'
    parser.add_argument('infile', type=argparse.FileType('r'), help=arg_help )

    arg_help = 'Id to select the person in the middle of the bow.'
    parser.add_argument('personid', type=str, help=arg_help )

    args = parser.parse_args()

    #results['format'] = args.format.lower()
    results['infile'] = args.infile.name
    results['personid'] = args.personid
    results['title'] = args.title.strip()
    results['iditem'] = args.iditem.lower()
    results['reverse'] = args.reverse_arrows
    results['ancestors'] = args.ancestors
    results['descendents'] = args.descendents
    results['from'] = args.fromgen
    results['dates'] = args.dates
    results['libpath'] = args.libpath

    # easy to get this one wrong, just drop back to default
    value = args.orientation.lower()
    if value in orientations:
       results['orientation'] = value

    return results


def get_indi_years( indi ):
    # return ( birth - death ) or (birth-) or (-death)
    # but None if both dates are empty

    def get_indi_year( indi_data, tag ):
        # "best" year for birth, death, ...
        # or an empty string
        result = ''

        best = 0
        if readgedcom.BEST_EVENT_KEY in indi_data:
           if tag in indi_data[readgedcom.BEST_EVENT_KEY]:
              best = indi_data[readgedcom.BEST_EVENT_KEY][tag]
        if tag in indi_data:
           if indi_data[tag][best]['date']['is_known']:
              result = str( indi_data[tag][best]['date']['min']['year'] )
        return result

    result = None

    birth = get_indi_year( data[ikey][indi], 'birt' ).strip()
    death = get_indi_year( data[ikey][indi], 'deat' ).strip()
    if birth or death:
       result = '(' + birth +'-'+ death + ')'

    return result


def get_name( indi, style, line_break=' ' ):
    # ouput formats deal with text in different "styles" for non-ascii characters
    # GraphML can dispay HTML encodings.
    # Dot can also display HTML.

    result = 'none'

    if indi is not None:
       result = data[ikey][indi]['name'][0][style]
       if readgedcom.UNKNOWN_NAME in result:
          # change to word with no special characters
          result = 'unknown'
       else:
          # remove any suffix after the end slash
          result = re.sub( r'/[^/]*$', '', result ).replace('/','').strip()

          if style == 'html':
             # escape quotes
             result = result.replace('"','&quot;').replace("'","&rsquo;")

          if options['dates']:
             dates = get_indi_years( indi )
             if dates:
                result += line_break + dates

    return result


def get_name_dot( indi ):
    return get_name( indi, 'html', '\\n' )


def find_other_partner( indi, fam ):
    result = None

    other_partners = dict()
    other_partners['husb'] = 'wife'
    other_partners['wife'] = 'husb'

    other = None
    for partner in other_partners:
        if partner in data[fkey][fam]:
           if indi == data[fkey][fam][partner][0]:
              other = other_partners[partner]
              break

    if other:
       if other in data[fkey][fam]:
          result = data[fkey][fam][other][0]

    return result


def dot_header():
    print( 'digraph family {' )


def dot_setup( orientation, title ):
    print( 'node [shape=record];' )
    print( 'rankdir=' + orientation.upper() + ';' )
    if title:
       print( 'labelloc="t";' )
       print( 'label="' + title + '";' )


def dot_trailer():
    print( '}' )


def make_dot_itag( n ):
    return 'i' + str( n )


def make_dot_ftag( n ):
    return 'f' + str( n )


def dot_families( n, indi_nodes, fam_nodes ):
    for fam in the_families:
        if fam not in fam_nodes:

           n += 1
           fam_tag = make_dot_ftag( n )

           # 'u' matches center of family structure
           fam_nodes[fam] = { 'tag':fam_tag, 'key':'u' }

           names = dict()
           names['wife'] = '?'
           names['husb'] = '?'

           for partner in names:
               if partner in data[fkey][fam]:
                  person_id = data[fkey][fam][partner][0]
                  # first char of partner matches 'h' and 'w' in structure
                  indi_nodes[person_id] = { 'tag':fam_tag, 'key':partner[0:1] }
                  names[partner] = get_name_dot( person_id )

           out = fam_tag + ' [label="'
           out += '<h>' + names['husb']
           out += '|<u>|'  # potentially marriage date could go in here
           out += '<w>' + names['wife']
           out += '"];'
           print( out )

    return n


def dot_not_families( n, indi_nodes ):
    # not a parent or spouse
    for indi in the_individuals:
        if indi not in indi_nodes:
           # and the person is not in any of the families which are selected
           in_a_fam = False
           item = 'fams'
           if item in data[ikey][indi]:
              for fam in data[ikey][indi][item]:
                  if fam in the_families:
                     in_a_fam = True
                     break
           if not in_a_fam:
              n += 1
              tag = make_dot_itag(n)
              # 'i' matches structure
              indi_nodes[indi] = { 'tag':tag, 'key':'i' }

              out = tag + ' [label="'
              out += '<i>' + get_name_dot( indi )
              out += '"];'
              print( out )

    return n


def dot_connectors( indi_nodes, fam_nodes, reverse_links ):
    # connections from people to their parent unions

    already_drawn = []

    for indi in the_individuals:
        if 'famc' in data[ikey][indi]:
           child_of = data[ikey][indi]['famc'][0]
           if child_of in the_families:
              f_link = fam_nodes[child_of]['tag'] +':'+ fam_nodes[child_of]['key']
              i_link = indi_nodes[indi]['tag'] +':'+ indi_nodes[indi]['key']

              connect = str(f_link) + ':' + str(i_link)
              if connect not in already_drawn:
                 already_drawn.append( connect )

                 if reverse_links:
                    print( i_link + ' -> ' + f_link + ';' )
                 else:
                    print( f_link + ' -> ' + i_link + ';' )


def add_ancestors( indi, max_gen, desc_from_gen, n_gen ):
    global the_individuals
    global the_families
    global from_ancestors

    if n_gen <= max_gen:
       if 'famc' in data[ikey][indi]:
          fam = data[ikey][indi]['famc'][0]

          if fam not in the_families:
             the_families.append( fam )

             for partner in ['wife','husb']:
                 if partner in data[fkey][fam]:
                    parent_id = data[fkey][fam][partner][0]
                    if n_gen == desc_from_gen:
                       if parent_id not in from_ancestors:
                          from_ancestors.append( parent_id )
                    if parent_id not in the_individuals:
                       the_individuals.append( parent_id )
                       add_ancestors( parent_id, max_gen, desc_from_gen, n_gen+1 )


def add_descendents( indi, max_gen, n_gen ):
    global the_individuals
    global the_families

    if n_gen <= max_gen:
       if 'fams' in data[ikey][indi]:
          for fam in data[ikey][indi]['fams']:
              if fam not in the_families:
                 the_families.append( fam )
              if 'chil' in data[fkey][fam]:
                 for child in data[fkey][fam]['chil']:
                     if child not in the_individuals:
                        the_individuals.append( child )
                     add_descendents( child, max_gen, n_gen+1 )

              # need to also add the partner in this family
              # so that the family will be displayed
              # but do not travel down this person's descendents
              other = find_other_partner( indi, fam )
              if other is not None:
                 the_individuals.append( other )


def get_individuals( start, max_ancestors, max_descendents, desc_from_gen ):
    global the_individuals
    global the_families
    global from_ancestors

    result = True

    the_individuals.append( start )

    add_ancestors( start, max_ancestors, desc_from_gen, 1 )

    if max_descendents > 0:
       if desc_from_gen == 0:
          from_ancestors.append( start )

       if from_ancestors:
          for indi in from_ancestors:
              add_descendents( indi, max_descendents, 1 )

       else:
          # only an error if ancestors for descentants were expected
          if desc_from_gen > 0:
             result = False
             print( '', file=sys.stderr )

    return result


def output_data( out_format ):
    result = True

    # put each person into a node
    # and each family also
    n_nodes = 0

    # by creating a new list
    indi_nodes = dict()
    fam_nodes = dict()

    if out_format == 'dot':
       dot_header()
       dot_setup( options['orientation'], options['title'] )

       n_nodes = dot_families( n_nodes, indi_nodes, fam_nodes )
       n_nodes = dot_not_families( n_nodes, indi_nodes )
       dot_connectors( indi_nodes, fam_nodes, options['reverse'] )

       dot_trailer()

    else:
       # unlikely to get here, but just in case i've made a typo
       print( 'Unknown format', out_format, file=sys.stderr )
       result = False

    return result


def data_ok():
    result = False
    # it is possible to have a tree with no families,
    # but individuals are required
    if ikey in data:
       if len( data[ikey] ) > 0:
          result = True
       else:
          print( 'Data is empty', file=sys.stderr )
    else:
       print( 'Data not correct format.', file=sys.stderr )
    return result


def options_ok( program_options ):
    result = True

    for item in ['ancestors','descendents','from']:
        if program_options[item] < 0:
           result = False
           print( 'Option', item, 'must be zero or more.', file=sys.stderr )

    if program_options['from'] > program_options['ancestors']:
       result = False
       print( 'Not enough ancestor generations selected for descendants', file=sys.stderr )

    return result


#def show_people( list_of_indi ):#debug
#    for indi in list_of_indi:
#        print( get_name( indi, 'value' ), '@i' + str(data[ikey][indi]['xref']) + '@', file=sys.stderr )
#def show_fam( list_of_fam ): #debug
#    for fam in list_of_fam:
#        output = ''
#        space = ''
#        for partner in ['wife','husb']:
#            if partner in data[fkey][fam]:
#               partner_id = data[fkey][fam][partner][0]
#               output += space + get_name( partner_id, 'value' )
#               space = ' + '
#        print( output, '@f' + str(data[fkey][fam]['xref']) + '@', file=sys.stderr )


options = get_program_options()

if not os.path.isdir( options['libpath'] ):
   print( 'Path to readgedcom is not a directory', file=sys.stderr )
   sys.exit( 1 )

readgedcom = load_my_module( 'readgedcom', options['libpath'] )

ikey = readgedcom.PARSED_INDI
fkey = readgedcom.PARSED_FAM

data = readgedcom.read_file( options['infile'] )

# find the people that should be output
the_individuals = []
the_families = []
from_ancestors = []

exit_code = 1

if data_ok():
   if options_ok( options ):
      start_person = readgedcom.find_individuals( data, options['iditem'], options['personid'] )
      if len(start_person) == 1:
         if get_individuals( start_person[0], options['ancestors'], options['descendents'], options['from'] ):
            if output_data( options['format'] ):
               exit_code = 0
            #print( 'start', file=sys.stderr ) #debug
            #show_people( start_person ) #debug
            #print( 'anc', options['ancestors'], 'desc', options['descendents'], 'from', options['from'], file=sys.stderr ) #debug
            #print( 'showing who is found', file=sys.stderr ) #debug
            #print( ', file=sys.stderr' )
            #print( 'indiv', the_individuals, file=sys.stderr ) #debug
            #show_people( the_individuals ) #debug
            #print( '', file=sys.stderr )
            #print( 'fam', the_families, file=sys.stderr ) #debug
            #show_fam( the_families ) #debug
            #print( '', file=sys.stderr )
            #print( 'from', from_ancestors, file=sys.stderr ) #debug
            #show_people( from_ancestors ) #debug

      else:
         if len(start_person) < 1:
            mess = 'Start person was not found'
         else:
            mess = 'More than 1 person matches start person'
         print( mess, options['personid'], options['iditem'], file=sys.stderr )

sys.exit( exit_code )
