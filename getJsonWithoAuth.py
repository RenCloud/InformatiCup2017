import json


def getJson2(url, github):
    """

    :param url: Github URL of Given Repository from which data is interested
    :param github: github request with oAuth
    :return: Json Object of Repository Data
    """
    # Get Owner of the repository
    owner = url.split('/')[3]
    # Get Repository Name
    repos = url.split('/')[4]
    # Request the Tree data recursive of given Repository
    r = github.get('https://api.github.com/repos/' + owner + '/' + repos + '/git/trees/master?recursive=1')
    # if request ok
    if r.ok:
        # create object from JSON response
        repoItemTree = json.loads(r.text or r.content)

    # if tree empty-> all empty
    # if object later empty set ???

    # Request Readme Data
    r = github.get('https://api.github.com/repos/' + owner + '/' + repos + '/readme')
    if r.ok:
        # ReadmeDataJson -> object
        repoItemReadme = json.loads(r.text or r.content)
        # Download Readme
        readme = github.get(
            'https://raw.githubusercontent.com/' + owner + '/' + repos + '/master/' + repoItemReadme['name']).text

    # Request Language Data
    r = github.get('https://api.github.com/repos/' + owner + '/' + repos + '/languages')
    if r.ok:
        # LanguageJson -> object
        repoItemLanguage = json.loads(r.text or r.content)

    # Request Commits Data ( up to 100 commits)
    r = github.get('https://api.github.com/repos/' + owner + '/' + repos + '/commits?per_page=100')
    if r.ok:
        # CommitJson -> Object
        repoItemCommits = json.loads(r.text or r.content)

    # Request Comments Data ( up to 100)
    r = github.get('https://api.github.com/repos/' + owner + '/' + repos + '/comments?per_page=100')
    if r.ok:
        # CommentJson -> Object
        repoItemsComment = json.loads(r.text or r.context)

    # Request Ussue Data ( Up to 100)
    r = github.get('https://api.github.com/repos/' + owner + '/' + repos + '/issues?per_page=100')
    if r.ok:
        # IssueJson -> Object
        repoItemIssue = json.loads(r.text or r.context)
    # Request Repo Infos
    r = github.get('https://api.github.com/repos/' + owner + '/' + repos)
    if r.ok:
        # InfoJson -> Object
        repoInfo = json.loads(r.text or r.context)

    # Convert all Object to JSON
    infoJson = json.dumps(repoInfo)
    treeJson = json.dumps(repoItemTree)
    readmeJson = '{\n"readme":' + json.dumps(readme) + '\n}'
    languageJson = json.dumps(repoItemLanguage)
    commitsJson = json.dumps(repoItemCommits)
    commentsJson = json.dumps(repoItemsComment)
    issueJson = json.dumps(repoItemIssue)
    # Create one Big JSON File
    finalReposItem = '[' + infoJson + ',' + treeJson + ',' + readmeJson + ',' + languageJson + ',' + commitsJson + ',' + commentsJson + ',' + issueJson + ']'
    # return the Big JSON File
    return finalReposItem


