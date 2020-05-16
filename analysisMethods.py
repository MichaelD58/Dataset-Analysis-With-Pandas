import pandas as pd
import numpy as np

def initialAnalysis(df):
    print("--- Initial descriptive analysis --- ")
    print("Total number of entries: " + str(len(df.index)))
    print("Earliest revision date: " + str(df.timestamp.min()))
    print("Latest revision date: " + str(df.timestamp.max()))
    print("Number of records by ID type: ")
    idtotals = {'ID': ['PMID', 'PMCID', 'DOI', 'ISBN', 'ARXIV'], 'Number of entries': [len(df.loc[df["type"] == "pmid"]), len(df.loc[df["type"] == "pmc"]), len(df.loc[df["type"] == "doi"]), len(df.loc[df["type"] == "isbn"]), len(df.loc[df["type"] == "arxiv"])] }
    idframe = pd.DataFrame(data=idtotals)
    print(idframe.to_string(index=False))

# Easy 1 - Output a table with the percentage of records for each identifier type
def IDTypePercentages(df):
    
    # Utility method for Easy 1
    def getPercentage(df, column):
        mypercent = round(float(len(column) * 100 / len(df.index)), 2)
        return mypercent

    print("Percentage of records by ID type: ")
    idtotals = {'ID': ['PMID', 'PMCID', 'DOI', 'ISBN', 'ARXIV'], 'Percentage of entries': [ getPercentage(df, df.loc[df["type"] == "pmid"]), getPercentage(df, df.loc[df["type"] == "pmc"]), getPercentage(df, df.loc[df["type"] == "doi"]), getPercentage(df, df.loc[df["type"] == "isbn"]), getPercentage(df, df.loc[df["type"] == "arxiv"])] }
    idframe = pd.DataFrame(data=idtotals)
    print(idframe.to_string(index=False))



#Easy2 - Calculate an average number of days since citation appeared on Wikipedia, as on March 1,2018
def avgDaysSinceAppearance(df):
    end_date = pd.to_datetime('2018-03-01 00:00:00')
    df["duration"] = (end_date -  df["timestamp"]).dt.days + 1
    print("Average number of days since citation appeared on Wikipedia, as on March 1 2018:")
    avg = df["duration"].mean()
    print(round(avg,2))


# Easy 3 - Output a table with the number of citations from arXiv by the year of their appearance
def arxivByYear(df):
    arxivFrame = df.loc[df["type"] == "arxiv"]
    arxiv_years = arxivFrame["timestamp"].dt.year.value_counts()
    print("Number of citations from arXiv by year:")
    print(arxiv_years.to_string())


# Medium 1 - Find  an  average  number  of  citations  per  page
def avgCitationsPerPage(df):
    print("Average number of citations per page: ")
    print(round(df["page_id"].value_counts().mean(), 2))
    print("Note - this does not include pages with zero citations (not present in data) ")

# Medium 2 - Find first ten pages citing the largest number of sources
def top10PagesWithMostSources(df):
    print("First ten pages citing the largest number of sources: ")
    df1 = pd.DataFrame({"Page id" : df["page_id"], "Page title" : df["page_title"],"Number of sources cited" : df.page_id.groupby(df.page_id).transform('count')})
    df1.drop_duplicates(inplace=True, subset="Page id")
    df1.sort_values(["Number of sources cited"], ascending=False, inplace=True)
    print(df1.head(10).to_string(index=False))

# Medium 3 - Output a table with the number of citations from Zenodo (https://zenodo.org/) by the year of their appearance
def zenodoByYear(df):
    df["zenodo"] = df.loc[df["type"] == "doi"].id.str.contains(pat='zenodo', na=False)
    df_zenodo = df.loc[df["zenodo"] == True]
    zenodo_years = df_zenodo["timestamp"].dt.year.value_counts()
    print("Number of citations from Zenodo (https://zenodo.org/) by the year of their appearance")
    print(zenodo_years.to_string())

#Hard 1 - Output a table with the number and percentage of citations appearing on Wikipedia by the number of years since their appearance
def citationsByYearsSinceAppearance(df):
    print("Number and percentage of citations appearing on Wikipedia by the number of years since their appearance:")
    current_year = pd.datetime.now().year
    df["years_since"] = current_year - df["timestamp"].dt.year
    df1 = pd.DataFrame({"Years since" : df["years_since"], "Number of citations" : df.years_since.groupby(df.years_since).transform('count')})
    df1.drop_duplicates(inplace=True)
    total = df1["Number of citations"].sum()
    percentage = (df1["Number of citations"] / total) * 100
    df1["Percentage of citations"] = round(percentage, 2)
    print(df1.sort_values(["Years since"]).to_string(index=False))

# Hard 2 - Find first ten most highly cited sources (for the given language version)
def top10MostCitedSources(df):
    print("10 most cited sources: ")
    df_tid = df.groupby(["type", "id"])
    typeIDFrame = df_tid.size().sort_values(ascending=False)
    print(typeIDFrame.head(10).to_string())

# All additional requirement methods combined into one 'additional descriptive analysis'
def additionalAnalysis(df):
    print("--- Additional descriptive analysis --- ")
    print("")
    IDTypePercentages(df)
    print("")
    avgDaysSinceAppearance(df)
    print("")
    arxivByYear(df)
    print("")
    avgCitationsPerPage(df)
    print("")
    top10PagesWithMostSources(df)
    print("")
    zenodoByYear(df)
    print("")
    citationsByYearsSinceAppearance(df)
    print("")
    top10MostCitedSources(df)
    print("")
