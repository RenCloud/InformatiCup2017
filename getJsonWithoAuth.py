import json


def getJson(url, github):
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
        # get up to 1000 commits with the header that comes back from github api
        stringcommiter = ''
        try:
            # get header / try to get him ( when it's only 1 page this header wont exist
            headers = r.headers['link']
            # split header data in smaller parts
            test = headers.split(',')
            # get page part of an smaller part ( smaler part is nearly a link and from the end of the link i want the
            #  number)
            startIndex = test[1].find('&page=')
            # get the last to chars -> if we have 2-9 whe cut it
            # if we have 10-99 -> 10-99
            # if the number bigger we have 130 or something -> 13 so 13x the last number is not interestet
            # we can do this becouse we want only 10 and very number bigger 99 will give us 10 or an bigger number than
            end = test[1][startIndex + 6:startIndex + 6 + 2]
            if end[1] == '>':
                end = end[0]
            # so if the number of pages smaller than 10 we use end as limit to get nearly the same json file like
            # through the C# application we can't use the Python json function so this makes json we need
            if int(end) < 10:
                repoItemCommits = json.loads(r.text or r.content)

                for i in repoItemCommits:
                    author = i['author']['login']
                    commiter = i['committer']['login']
                    stringcommiter += '{"author_login": "' + author + '","commiter_login": "' + commiter + '"},'

                for i in range(2, int(end) + 1):
                    r = github.get(
                        'https://api.github.com/repos/' + owner + '/' + repos + '/commits?per_page=100&page=' + str(i))
                    repoItemCommits += json.loads(r.text or r.content)

                    for singleCommit in repoItemCommits:
                        author = singleCommit['author']['login']
                        commiter = singleCommit['committer']['login']
                        stringcommiter += '{"author_login": "' + author + '","commiter_login": "' + commiter + '"},'

            else:
                # if end is 10 or up we us a fix range [2 -11) to get 10 pages
                repoItemCommits = json.loads(r.text or r.content)

                for i in repoItemCommits:
                    author = i['author']['login']
                    commiter = i['committer']['login']
                    stringcommiter += '{"author_login": "' + author + '","commiter_login": "' + commiter + '"},'

                for i in range(2, 11):
                    r = github.get(
                        'https://api.github.com/repos/' + owner + '/' + repos + '/commits?per_page=100&page=' + str(i))
                    repoItemCommits += json.loads(r.text or r.content)
                    for singleCommit in repoItemCommits:
                        author = singleCommit['author']['login']
                        commiter = singleCommit['committer']['login']
                        stringcommiter += '{"author_login": "' + author + '","commiter_login": "' + commiter + '"},'

            # to have an valide json string/file we need to cut the last ',' up, becouse every new item have a ',
            # ' at the end of the string but the last have none so this must cut
            stringcommiter = stringcommiter[0:len(stringcommiter) - 1]
        except:
            # is within the header no 'link' object the commit page is the only one -> we does not need to run
            # through more pages
            repoItemCommits = json.loads(r.text or r.content)
            j = 0
            for i in repoItemCommits:

                try:
                    # again here to create a valid json we must create it for us self

                    # but know the last add wont add a ',' to the string so we does not need to cut it
                    author = i['author']['login']
                    commiter = i['committer']['login']
                    if j < (len(repoItemCommits) - 1):
                        stringcommiter += '{"author_login": "' + author + '","commiter_login": "' + commiter + '"},'
                    else:
                        stringcommiter += '{"author_login": "' + author + '","commiter_login": "' + commiter + '"}'
                    j += 1
                except:
                    # count also when a problem is there so we have no other problems ;D
                    j += 1

    # Request Comments Data ( up to 100)
    r = github.get('https://api.github.com/repos/' + owner + '/' + repos + '/comments?per_page=100')
    if r.ok:
        # same heere like above only for other data
        # also we does not create on us self the json file
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

    # Request issue Data ( Up to 100)
    r = github.get('https://api.github.com/repos/' + owner + '/' + repos + '/issues?per_page=100')
    if r.ok:
        # again work through all possible pages up to 10 and  create nromal json file
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

    # the normal json of inoJson is not that we need so we have to cut it and fix something
    infoJson = infoJson[1:len(infoJson) - 1]
    # tree data is also not 100 % correct
    treeJson = json.dumps(repoItemTree)
    # so we have find 'tree:' to replace it , the string bevour will cut and add change at the and '],' to ']'
    start = treeJson.find('"tree":')
    short = treeJson[start:len(treeJson)]
    short = short.replace('tree', 'repository', 1)
    end = short.find(']')
    treeJson = short[0:end + 1]
    # the data that is in readmes contains not correct character so we need to use json.dumps to filter them out
    readmeJson = '"readme":' + json.dumps(readme)
    languageJson = '"languages":' + json.dumps(repoItemLanguage)
    commitsJson = '"commits":[' + stringcommiter + ']'
    commentsJson = '"comments":' + json.dumps(repoItemsComment)
    issueJson = '"issues":' + json.dumps(repoItemIssue)
    # Create one Big JSON File
    # add '{' '}' at the and and beginn to creaet a valid json file and ',' between parts
    finalReposItem = '{' + infoJson + ',' + treeJson + ',' + readmeJson + ',' + languageJson + ',' + commitsJson + ',' + commentsJson + ',' + issueJson + '}'
    # return the Big JSON File
    return finalReposItem
