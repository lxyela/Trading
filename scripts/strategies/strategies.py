# calculte the support and resistance levels for the given data
#
# input:
#   data: pandas dataframe
#   period: number of days to calculate the support and resistance levels
#   n: number of support and resistance levels to calculate
# output:
#   support: pandas dataframe with the support levels
#   resistance: pandas dataframe with the resistance levels
def support_and_resistance(data, period=14, n=2):
    # calculate the highest high and lowest low for the given period
    data['highest_high'] = data['High'].rolling(window=period).max()
    data['lowest_low'] = data['Low'].rolling(window=period).min()
    
    # calculate the support and resistance levels
    data['support'] = data['lowest_low'].rolling(window=n).min()
    data['resistance'] = data['highest_high'].rolling(window=n).max()
    
    # drop the columns with null values
    data = data.drop(['highest_high', 'lowest_low'], axis=1)
    
    # return the support and resistance levels
    return data['support'], data['resistance']