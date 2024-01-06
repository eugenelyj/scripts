import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from collections import OrderedDict

# List of words that should not be capitalized in titles
WORDS_TO_NOT_CAPITALIZE = {'of', 'and', 'in', 'on', 'for', 'with', 'a', 'an', 'the', 'at', 'by', 'from', 'to'}

# Predefined mapping rules
MAPPING_RULES = {
    frozenset(['icra', 'international conference on robotics and automation']): 'In the Proceedings of IEEE International Conference on Robotics and Automation',
    frozenset(['iros', 'intelligent robots and systems']): 'In the Proceedings of IEEE/RSJ International Conference on Intelligent Robots and Systems',
    frozenset(['iccv', 'international conference on computer vision']): 'In the Proceedings of IEEE/CVF International Conference on Computer Vision',
    frozenset(['cvpr', 'computer vision and pattern recognition']): 'In the Proceedings of IEEE/CVF Conference on Computer Vision and Pattern Recognition',
    frozenset(['eccv', 'european conference on computer vision']): 'In the Proceedings of European Conference on Computer Vision',
    frozenset(['icml', 'international conference on machine learning']): 'In the Proceedings of International Conference on Machine Learning',
    frozenset(['nips', 'neural information processing systems']): 'In the Proceedings of Advances in Neural Information Processing Systems',
    frozenset(['aaai', 'association for the advancement of artificial intelligence']): 'In the Proceedings of AAAI Conference on Artificial Intelligence',
    frozenset(['ijcai', 'international joint conference on artificial intelligence']): 'In the Proceedings of International Joint Conference on Artificial Intelligence',
    frozenset(['iclr', 'international conference on learning representations']): 'In the Proceedings of International Conference on Learning Representations',
    frozenset(['rss', 'robotics: science and systems']): 'In the Proceedings of Robotics: Science and Systems',
    frozenset(['pami', 'ieee transactions on pattern analysis and machine intelligence']): 'IEEE Transactions on Pattern Analysis and Machine Intelligence',
    frozenset(['ijcv', 'international journal of computer vision']): 'International Journal of Computer Vision',
    frozenset(['mm', 'acm multimedia']): 'In the Proceedings of ACM International Conference on Multimedia',
    frozenset(['ral', 'ieee robotics and automation letters']): 'IEEE Robotics and Automation Letters',
    frozenset(['corl', 'conference on robot learning']): 'In the Proceedings of Conference on Robot Learning',
    frozenset(['siggraph', 'special interest group on computer graphics and interactive techniques']): 'In the Proceedings of ACM SIGGRAPH Conference on Computer Graphics and Interactive Techniques',
    frozenset(['siggraph asia', 'special interest group on computer graphics and interactive techniques asia']): 'In the Proceedings of ACM SIGGRAPH Asia Conference on Computer Graphics and Interactive Techniques',
    frozenset(['tog', 'acm transactions on graphics']): 'ACM Transactions on Graphics',
    frozenset(['tvcg', 'ieee transactions on visualization and computer graphics']): 'IEEE Transactions on Visualization and Computer Graphics',
    frozenset(['tip', 'ieee transactions on image processing']): 'IEEE Transactions on Image Processing',
    frozenset(['miccai', 'medical image computing and computer assisted intervention']): 'In the Proceedings of International Conference on Medical Image Computing and Computer Assisted Intervention',
    frozenset(['ismar', 'international symposium on mixed and augmented reality']): 'In the Proceedings of IEEE International Symposium on Mixed and Augmented Reality',
    frozenset(['vr', 'virtual reality']): 'In the Proceedings of IEEE Conference on Virtual Reality and 3D User Interfaces',
    frozenset(['3dv', 'international conference on 3d vision']): 'In the Proceedings of International Conference on 3D Vision',
    frozenset(['wacv', 'winter conference on applications of computer vision']): 'In the Proceedings of IEEE Winter Conference on Applications of Computer Vision',
    frozenset(['accv', 'asian conference on computer vision']): 'In the Proceedings of Asian Conference on Computer Vision',
    frozenset(['tro', 'ieee transactions on robotics']): 'IEEE Transactions on Robotics',
}


def apply_mapping_rules(entry, field):
    if field in entry:
        original_value = entry[field].lower()
        original_value = original_value.replace('{', '')
        original_value = original_value.replace('}', '')

        contains_workshop = 'workshop' in original_value
        for key, mapped_value in MAPPING_RULES.items():
            flag = False
            for keyword in key:
                if keyword in original_value:
                    if contains_workshop:
                        mapped_value += ' Workshops'
                    entry[field] = f'{{{mapped_value}}}'
                    flag = True
                    break
            if flag:
                break


def capitalize_word(word):
    # Split the word if it contains a dash and capitalize only the first part
    if '-' in word:
        parts = word.split('-')
        return '-'.join([parts[0].capitalize()] + parts[1:])
    else:
        return word if word in WORDS_TO_NOT_CAPITALIZE else word.capitalize()

def capitalize_first_word(word):
    # Capitalize only the first letter of the first word
    return word[0].upper() + word[1:] if word else word

def capitalize_title(title):
    title = title.replace('{', '')
    title = title.replace('}', '')
    
    words = title.split()
    capitalized_words = [capitalize_first_word(words[0])] + [capitalize_word(word) for word in words[1:]]
    title = ' '.join(capitalized_words)

    title = title.replace('3d', '3D')
    title = title.replace('2d', '2D')

    return f'{{{title}}}'

def capitalize_titles(bib_data):
    for entry in bib_data.entries:
        if 'title' in entry:
            entry['title'] = capitalize_title(entry['title'])

def process_pub(bib_data):
    for entry in bib_data.entries:
        apply_mapping_rules(entry, 'booktitle')
        apply_mapping_rules(entry, 'journal')

def read_and_capitalize_titles(file_path):
    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
    parser.homogenise_fields = False
    parser.alt_dict = OrderedDict  # Use OrderedDict to maintain entry order
    with open(file_path, encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file, parser=parser)
    
    capitalize_titles(bib_database)
    process_pub(bib_database)

    return bib_database

def write_bib_file(bib_database, output_file_path):
    writer = BibTexWriter()
    writer.order_entries_by = None  # Preserve the original order of entries
    with open(output_file_path, 'w', encoding='utf-8') as bibtex_file:
        bibtex_file.write(writer.write(bib_database))

# Update these file paths as necessary
input_file_path = 'body/ref.bib.bk'  # Path to your .bib file
output_file_path = 'body/ref.bib'  # Path to save the modified .bib file

# Process the file
bib_database = read_and_capitalize_titles(input_file_path)
write_bib_file(bib_database, output_file_path)
