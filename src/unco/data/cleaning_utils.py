def replace_value_by_mean(df, column, value):
    temp = df[df[column] != value]
    mean = temp[column].mean()
    
    indices = df[df[column] == value].index
    df.loc[indices, column] = mean
