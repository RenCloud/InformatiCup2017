namespace GitRepoToJSON.Models
{
    public struct JSONFullData
    {
        public int id;
        public string name;
        public string full_name;
        public int owner_id;
        public string description;
        public string readme;
        public Language[] language;
        public Repro[] repository;
        public bool truncated;
        public Commits[] commits;
        public Comments[] comments;
        public Issue[] issue;

        public JSONFullData(int id, string name, string fullName, int ownerId, string description, string readme, Language[] language, Repro[] repository, bool truncated, Commits[] commits, Comments[] comments, Issue[] issue)
        {
            this.id = id;
            this.name = name;
            full_name = fullName;
            owner_id = ownerId;
            this.description = description;
            this.readme = readme;
            this.language = language;
            this.repository = repository;
            this.truncated = truncated;
            this.commits = commits;
            this.comments = comments;
            this.issue = issue;
        }
    }

    public struct Language
    {
        public string lang;
        public long bytes;

        public Language(string lang, long bytes)
        {
            this.lang = lang;
            this.bytes = bytes;
        }
    }

    public struct Repro
    {
        public string path;
        public string type;

        public Repro(string path, string type)
        {
            this.path = path;
            this.type = type;
        }
    }

    public struct Commits
    {
        public Commit commit;
        public string author_login;
        public string committer_login;

        public Commits(Commit commit, string authorLogin, string committerLogin)
        {
            this.commit = commit;
            author_login = authorLogin;
            committer_login = committerLogin;
        }
    }

    public struct Commit
    {
        public Author author;
        public Author commiter;
        public string message;

        public Commit(Author author, Author commiter, string message)
        {
            this.author = author;
            this.commiter = commiter;
            this.message = message;
        }
    }

    public struct Author
    {
        public string name;
        public string email;

        public Author(string name, string email)
        {
            this.name = name;
            this.email = email;
        }
    }

    public struct Comments
    {
        public string body;
        public string path;
        public Author user;

        public Comments(string body, string path, Author user)
        {
            this.body = body;
            this.path = path;
            this.user = user;
        }
    }

    public struct Issue
    {
        public string state;
        public string title;
        public string body;
        public Author user;


        public Issue(string state, string title, string body, Author user)
        {
            this.state = state;
            this.title = title;
            this.body = body;
            this.user = user;

        }
    }
}