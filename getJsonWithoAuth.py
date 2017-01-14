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
    else:
        r = github.get('https://api.github.com/repos/' + owner + '/' + repos)
        if r.ok:
            return json.dumps(json.loads(r.text or r.context))
        else:
            return None
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
        stringcommiter = ''
        try:
            headers = r.headers['link']
            test = headers.split(',')
            startIndex = test[1].find('&page=')
            end = test[1][startIndex+6:startIndex+6+2]
            if end[1] == '>':
                end = end[0]

            if int(end)<10:
                repoItemCommits = json.loads(r.text or r.content)

                for i in repoItemCommits:
                    author = i['author']['login']
                    commiter = i['committer']['login']
                    stringcommiter += '{"author_login": "' + author + '","commiter_login": "' + commiter + '"},'




                for i in range(2, int(end)+1):
                    r = github.get(
                        'https://api.github.com/repos/' + owner + '/' + repos + '/commits?per_page=100&page=' + str(i))
                    repoItemCommits += json.loads(r.text or r.content)

                    for i in repoItemCommits:
                        author = i['author']['login']
                        commiter = i['committer']['login']
                        stringcommiter += '{"author_login": "' + author + '","commiter_login": "' + commiter + '"},'



            else:
                repoItemCommits = json.loads(r.text or r.content)

                for i in repoItemCommits:
                    author = i['author']['login']
                    commiter = i['committer']['login']
                    stringcommiter += '{"author_login": "' + author + '","commiter_login": "' + commiter + '"},'


                for i in range(2, 11):
                    r = github.get('https://api.github.com/repos/' + owner + '/' + repos + '/commits?per_page=100&page=' + str(i))
                    repoItemCommits += json.loads(r.text or r.content)
                    for i in repoItemCommits:
                        author = i['author']['login']
                        commiter = i['committer']['login']
                        stringcommiter += '{"author_login": "' + author + '","commiter_login": "' + commiter + '"},'





            stringcommiter = stringcommiter[0:len(stringcommiter)-1]
        except:
            repoItemCommits = json.loads(r.text or r.content)
            j = 0
            for i in repoItemCommits:

                try:

                    author = i['author']['login']
                    commiter = i['committer']['login']
                    if j < (len(repoItemCommits) - 1):
                        stringcommiter += '{"author_login": "' + author + '","commiter_login": "' + commiter + '"},'
                    else:
                        stringcommiter += '{"author_login": "' + author + '","commiter_login": "' + commiter + '"}'
                    j=j+1
                except:

                    j=j+1


    # Request Comments Data ( up to 100)
    r = github.get('https://api.github.com/repos/' + owner + '/' + repos + '/comments?per_page=100')
    if r.ok:

        try:
            headers = r.headers['link']
            test = headers.split(',')
            startIndex = test[1].find('&page=')
            end = test[1][startIndex + 6:startIndex + 6 + 2]
            if end[1] == '>':
                end = end[0]

            if int(end) < 10:
                repoItemsComment = json.loads(r.text or r.content)
                for i in range(2, int(end) + 1):
                    r = github.get(
                        'https://api.github.com/repos/' + owner + '/' + repos + '/comments?per_page=100&page=' + str(i))
                    repoItemsComment += json.loads(r.text or r.content)



            else:
                repoItemsComment = json.loads(r.text or r.content)
                for i in range(2, 11):
                    r = github.get(
                        'https://api.github.com/repos/' + owner + '/' + repos + '/comments?per_page=100&page=' + str(i))
                    repoItemsComment += json.loads(r.text or r.content)





        except:
            repoItemsComment = json.loads(r.text or r.content)

    # Request Ussue Data ( Up to 100)
    r = github.get('https://api.github.com/repos/' + owner + '/' + repos + '/issues?per_page=100')
    if r.ok:

        try:
            headers = r.headers['link']
            test = headers.split(',')
            startIndex = test[1].find('&page=')
            end = test[1][startIndex + 6:startIndex + 6 + 2]
            if end[1] == '>':
                end = end[0]

            if int(end) < 10:
                repoItemIssue = json.loads(r.text or r.content)
                for i in range(2, int(end) + 1):
                    r = github.get(
                        'https://api.github.com/repos/' + owner + '/' + repos + '/issues?per_page=100&page=' + str(i))
                    repoItemIssue += json.loads(r.text or r.content)



            else:
                repoItemIssue = json.loads(r.text or r.content)
                for i in range(2, 11):
                    r = github.get(
                        'https://api.github.com/repos/' + owner + '/' + repos + '/issues?per_page=100&page=' + str(i))
                    repoItemIssue += json.loads(r.text or r.content)





        except:
            repoItemIssue = json.loads(r.text or r.content)
    # Request Repo Infos
    r = github.get('https://api.github.com/repos/' + owner + '/' + repos)
    if r.ok:
        # InfoJson -> Object
        repoInfo = json.loads(r.text or r.context)

    # Convert all Object to JSON
    infoJson = json.dumps(repoInfo)
    infoJson = infoJson[1:len(infoJson)-1]

    treeJson = json.dumps(repoItemTree)
    start = treeJson.find('"tree":')
    short = treeJson[start:len(treeJson)]
    short = short.replace('tree','repository',1)
    end = short.find(']')
    treeJson = short[0:end+1]
    readmeJson = '"readme":' + json.dumps(readme)
    languageJson = '"languages":'+json.dumps(repoItemLanguage)
    commitsJson = '"commits":['+stringcommiter+']'
    commentsJson = '"comments":'+json.dumps(repoItemsComment)
    issueJson = '"issues":'+json.dumps(repoItemIssue)
    # Create one Big JSON File
    finalReposItem = '{' + infoJson + ',' + treeJson + ',' + readmeJson + ',' + languageJson + ',' + commitsJson + ',' + commentsJson + ',' + issueJson + '}'
    # return the Big JSON File
    return finalReposItem


