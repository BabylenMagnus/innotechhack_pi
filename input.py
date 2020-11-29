import sys
import vk
from data_parsing import add_encoding


test = vk.get_users_data([sys.argv[1].split('/')[-1]])
add_encoding(test['response'][0])
