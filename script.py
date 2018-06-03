import sys


def _file_to_tab(file):
    tab = []
    for line in file:
        line = line.rstrip('\r\n')
        features = line.split()
        if len(features) == 0:
            tab.append([''])
        else:
            tab.append(features)
    return tab


def _find_shift_a(expected_tab, result_tab, index_exp, index_res):
    decal_exp = 0
    decal_res = 0
    try:
        exp_fea = expected_tab[index_exp]
    except IndexError, e:
        return

    try:
        res_fea = result_tab[index_res]
    except IndexError, e:
        return

    if res_fea[0] in exp_fea[0] and len(exp_fea[0]) > len(res_fea[0]):
        look = True
        exp_word = exp_fea[0]
        i = 0
        # decal_res
        while look:
            res_fea = result_tab[index_res + decal_res]
            res_word = res_fea[0]
            if res_word not in exp_fea[0] or len(exp_fea[0]) < len(res_word):
                break
            j = 0
            while j < len(res_word):
                if res_word[j] == exp_word[i]:
                    if i == len(exp_word) - 1:
                        if j == len(res_word) - 1:
                            return 1, decal_res + 1
                        # elif j > 1:
                            # je ne sais pas
                        else:
                            look = False
                            break

                    elif i < len(exp_word):
                        i += 1
                    j += 1
                else:
                    look = False
                    break
            decal_res += 1

    elif exp_fea[0] in res_fea[0] and len(exp_fea[0]) < len(res_fea[0]):
        look = True
        res_word = res_fea[0]
        i = 0
        # decal_res
        while look:
            exp_fea = expected_tab[index_exp + decal_exp]
            exp_word = exp_fea[0]
            if exp_word not in res_word or len(exp_word) > len(res_word):
                break
            j = 0
            while j < len(exp_word):
                if exp_word[j] == res_word[i]:
                    if i == len(res_word) - 1:
                        if j == len(exp_word) - 1:
                            return decal_exp + 1, 1
                        else:
                            look = False
                            break

                    elif i < len(res_word):
                        i += 1
                    j += 1
                else:
                    look = False
                    break
            decal_exp += 1

    return _find_shift(expected_tab, result_tab, index_exp, index_res)


def _find_shift(expected_tab, result_tab, index_exp, index_res):
    decal_exp = 0
    decal_res = 0

    try:
        exp_fea = expected_tab[index_exp]
    except IndexError, e:
        return

    try:
        res_fea = result_tab[index_res]
    except IndexError, ie:
        res_fea = result_tab[index_res - 1]

    # Case just one shift
    # shift exp
    for shift in range(0, 20):
        decal_exp = shift
        exp_fea = expected_tab[index_exp + decal_exp]
        # res_fea = result_tab[index_res]
        if exp_fea[0] != '' and res_fea[0] != '':
            if exp_fea[0] == res_fea[0]:
                return decal_exp, 0

    # shift res
    exp_fea = expected_tab[index_exp]
    for shift in range(0, 20):
        decal_res = shift
        res_fea = result_tab[index_res + decal_res]
        if exp_fea[0] != '' and res_fea[0] != '':
            if exp_fea[0] == res_fea[0]:
                return 0, decal_res


    # Case both shift
    # shift exp
    res_fea = result_tab[index_res + 1]
    for shift in range(0, 20):
        decal_exp = shift
        exp_fea = expected_tab[index_exp + decal_exp]
        if exp_fea[0] != '' and res_fea[0] != '':
            if exp_fea[0] == res_fea[0]:
                return decal_exp, 1

    # shift res
    exp_fea = expected_tab[index_exp + 1]
    for shift in range(0, 20):
        decal_res = shift
        res_fea = result_tab[index_res + decal_res]
        if exp_fea[0] != '' and res_fea[0] != '':
            if exp_fea[0] == res_fea[0]:
                return 1, decal_res


    return 1, 1


def add_result_to_expected(expected_tab, result_tab):
    index_res = 0
    index_exp = -1
    errors = 0

    length = len(expected_tab)

    while index_exp < length:

        try:
            exp_fea = expected_tab[index_exp]
        except IndexError, e:
            return

        try:
            res_fea = result_tab[index_res]
            if len(res_fea) == 1:
                res_fea[0] = ''
        except IndexError, ie:
            res_fea = result_tab[index_res - 1]

        if exp_fea[0] == '':
            print
            if res_fea[0] == '':
                index_res += 1
            index_exp += 1
            continue
        elif res_fea[0] == '':
            index_res += 1
            continue
        elif exp_fea[0] == '-DOCSTART-':
            index_exp += 1
            continue
        elif exp_fea[0] == res_fea[0]:
            index_res += 1
            index_exp += 1
            continue
        else:
            errors += 1
            decal_exp = 0
            decal_res = 0
            try:
                decal_exp, decal_res = _find_shift_a(expected_tab, result_tab, index_exp, index_res)
            except Exception, e:
                pass
            for i in range(0, decal_exp):
                exp_fea = expected_tab[index_exp + i]
                if exp_fea[0] != '':
                    pass
            index_res += decal_res
            index_exp += decal_exp
    return errors

def merge_files(expected_file, result_file):

    expected_tab = _file_to_tab(expected_file)
    result_tab = _file_to_tab(result_file)

    try:
        print add_result_to_expected(expected_tab, result_tab)
    except:
        pass


# Open the results
def main(argv):

    with open(sys.argv[1]) as expected_file:
        with open(sys.argv[2]) as result_file:
            merge_files(expected_file, result_file)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
