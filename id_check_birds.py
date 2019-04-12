import pandas as pd
main_ls = []
for i in range(15):
    filename = 'birds_' + str(i) + '.csv'
    ls = []
    with open(filename) as f:
        next(f)
        for row in f:
            if row != '\n':
                ls.append(row.split(',')[0])
            # import pdb; pdb.set_trace()
    ls.sort()
    main_ls.append(ls)

df = pd.DataFrame(main_ls)
# duplicateRowsDF = df[df.duplicated()] - there are some not duplicated because of new entrants or bikes that leave the radius.
