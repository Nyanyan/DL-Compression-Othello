
pattern_info = [
    # name, n_input_nodes, n_symmetry, normalize, n_variables, type
    
    ['line2', 16, 4, 1, 3 ** 8, 'disc_pattern'],
    ['line3', 16, 4, 1, 3 ** 8, 'disc_pattern'],
    ['line4', 16, 4, 1, 3 ** 8, 'disc_pattern'],
    ['diagonal5', 10, 4, 1, 3 ** 5, 'disc_pattern'],
    ['diagonal6', 12, 4, 1, 3 ** 6, 'disc_pattern'],
    ['diagonal7', 14, 4, 1, 3 ** 7, 'disc_pattern'],
    ['diagonal8', 16, 2, 1, 3 ** 8, 'disc_pattern'],
    ['corner9', 18, 4, 1, 3 ** 9, 'disc_pattern'],
    ['edge_2X', 20, 4, 1, 3 ** 10, 'disc_pattern'],
    ['triangle', 20, 4, 1, 3 ** 10, 'disc_pattern'],
    ['edge_block', 20, 4, 1, 3 ** 10, 'disc_pattern'],
    ['cross', 20, 4, 1, 3 ** 10, 'disc_pattern'],
    ['edge_2Y', 20, 4, 1, 3 ** 10, 'disc_pattern'],
    ['narrow_triangle', 20, 4, 1, 3 ** 10, 'disc_pattern'],
    ['fish', 20, 4, 1, 3 ** 10, 'disc_pattern'],
    ['kite', 20, 4, 1, 3 ** 10, 'disc_pattern'],

    ['n_surround', 2, 1, 64, 64 ** 2, 'additional_feature'],
    ['n_mobility', 2, 1, 35, 35 ** 2, 'additional_feature'],
    ['n_discs', 2, 1, 65, 65 ** 2, 'additional_feature'],

    ['mobility_line1', 16, 4, 1, 65536, 'mobility_pattern'],
    ['mobility_line2', 16, 4, 1, 65536, 'mobility_pattern'],
    ['mobility_line3', 16, 4, 1, 65536, 'mobility_pattern'],
    ['mobility_line4', 16, 4, 1, 65536, 'mobility_pattern']
]

print('n_paterns', len(pattern_info), 'n_param', sum(elem[4] for elem in pattern_info))