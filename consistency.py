import pandas as pd
import numpy as np

def removeInconsistentData(df):
    rows_before = len(df.index)

    df.dropna(inplace=True) # drop rows from the dataframe if they have any column with no data
    df.drop_duplicates(keep='first',inplace=True) # drops duplicate rows in the dataframe

    datatypes = list(df.dtypes)

    # page_id should be an int
    if (datatypes[0] != 'int'):
        df = df[df["page_id"].str.contains(pat="^\d*$", regex=True)]
        df["page_id"] = df["page_id"].astype('int')

    # page_title should be utf-8

    # rev_id should be an int
    if (datatypes[2] != 'int'):
        df = df[df["rev_id"].str.contains(pat="^\d*$", regex=True)]
        df["rev_id"] = df["rev_id"].astype('int')

    # date should be ISO 8601 datetime
    if (datatypes[3] != 'datetime64[ns]'):
        df = df[df["timestamp"].str.contains(pat="\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", regex=True)]
        df["timestamp"] = df["timestamp"].astype('datetime64[ns]')

    # type should be one of pmid/pmc/doi/isbn/arxiv
    df = df[df["type"].str.match(pat = "(pmid)|(pmc)|(doi)|(isbn)|(arxiv)")]
    df["type"] = df.type.astype("category") # reduces space taken up

    pieces = [df.loc[df["type"] == "pmid"], df.loc[df["type"] == "pmc"], df.loc[df["type"] == "doi"], df.loc[df["type"] == "isbn"], df.loc[df["type"] == "arxiv"]]

    # id should be utf-8
    # all non-conforming ids are filtered out

    # valid PMID are 1-8 digits
    pieces[0] = pieces[0][pieces[0].id.str.contains(pat="\d{1,8}", regex=True)]

    # valid PMCID are 1-7 digits
    pieces[1] = pieces[1][pieces[1].id.str.contains(pat="\d{7}", regex=True)]

    # valid DOI start with 10.NNNN where NNNN is a number > 1000, and then can have further .N, then /suffix
    pieces[2] = pieces[2][pieces[2].id.str.contains(pat="10.[1-9]\d{3}(?:.\d+)*/\w+", regex=True)]

    # valid ISBN are either 10 or 13 digits, if 13, they can only begin with 978/979                                                                                       
    pieces[3] = pieces[3][pieces[3].id.str.contains(pat="^(?:978|979)?\d{9}(?:X|\d)$", regex=True)]

    # valid ARXIV is either subject. 2 letters for the class (where applicable) then /YYMMnumber or YYMM.Number
    pieces[4] = pieces[4][pieces[4].id.str.contains(pat="(?:\w+-\w+.(?:[A-Z]{2})?\/)?(?:0[1-9]|1[012])(?:0[1-9]|1[012])(?:.)?\d*", regex=True)] 
    df = pd.concat(pieces)
    
    rows_after = len(df.index)

    percent_removed = ((rows_before-rows_after)/rows_before) * 100
    percent_removed_2dp = round(percent_removed, 2)
    print("Removed " + str(percent_removed_2dp) + "% percent of rows due to inconsistencies ")

    return df

def getTypesForCleanData(df):
    df["page_id"] = df["page_id"].astype('int')
    df["rev_id"] = df["rev_id"].astype('int')
    df["timestamp"] = df["timestamp"].astype('datetime64[ns]')
    df["type"] = df.type.astype("category")

    return df
